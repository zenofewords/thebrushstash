from decimal import Decimal

from django.apps import apps
from django.utils.text import slugify
from django.utils.translation import gettext as _

from shop.constants import (
    FREE_SHIPPING_PRICE,
    FREE_SHIPPING_PRODUCTS,
    TAX,
)
from thebrushstash.constants import (
    DEFAULT_COUNTRY,
    DEFAULT_CURRENCY,
    currency_symbol_mapping,
)
from thebrushstash.models import (
    Country,
    ExchangeRate,
)

defaultProductType = 'brush'


def get_default_product_type():
    ProductType = apps.get_model('shop', 'ProductType')

    try:
        return ProductType.objects.get(slug=defaultProductType).pk
    except ProductType.DoesNotExist:
        return None


def update_product_prices(product):
    exchange_rates = ExchangeRate.objects.all()

    if product.price_hrk:
        for er in exchange_rates:
            price = product.price_hrk + product.price_hrk * er.added_value / 100
            setattr(product, 'price_{}'.format(er.currency.lower()), price / er.middle_rate)

    if product.old_price_hrk:
        for er in exchange_rates:
            old_price = product.old_price_hrk + product.old_price_hrk * er.added_value / 100
            setattr(product, 'old_price_{}'.format(er.currency.lower()), old_price / er.middle_rate)


def update_product_rating(product):
    Review = apps.get_model('shop', 'Review')

    reviews = Review.published_objects.filter(product=product)
    product.ratings = reviews.count()
    product.score = sum([r.score for r in reviews])
    product.save()


def set_shipping_cost(bag, region, country_name=None):
    quantity_condition = int(bag.get('total_quantity', 0)) >= int(FREE_SHIPPING_PRODUCTS)
    cost_condition = Decimal(bag.get('total', 0)) >= Decimal(FREE_SHIPPING_PRICE)

    product_condition = False
    Product = apps.get_model('shop', 'Product')

    for product_name in bag.get('products'):
        product = Product.objects.filter(slug=slugify(product_name)).first()

        if product and product.free_shipping:
            product_condition = True
            break
    conditions = (quantity_condition or cost_condition or product_condition)
    free_shipping = conditions and country_name == DEFAULT_COUNTRY

    cost = 0
    if country_name:
        country = Country.published_objects.filter(name=country_name).first()
        cost = country.shipping_cost if country and country.shipping_cost else cost

    shipping_cost = Decimal('0.00') if free_shipping else Decimal(cost)

    bag['shipping_cost'] = str(shipping_cost)
    bag['grand_total'] = str(Decimal(bag.get('total', 0)) + shipping_cost)


def set_tax(bag, key_prefix=''):
    total = Decimal(bag.get('{}{}'.format(key_prefix, 'total'), 0))
    bag['{}{}'.format(key_prefix, 'tax')] = str(round(total - total / (Decimal(TAX) + 1), 2))


def get_totals(data, key, operator_param, product={}, quantity=None):
    quantity = quantity if quantity else data.get('quantity')

    price_hrk = Decimal(data.get('price_hrk'))
    subototal = quantity * price_hrk
    prices = {'price_hrk': str(price_hrk)} if key == 'subtotal' else {}

    if product:
        return {'{}'.format(key): str(operator_param(Decimal(product.get('{}'.format(key))), subototal))}
    else:
        return {
            '{}'.format(key): str(subototal),
            **prices,  # noqa
        }


def get_grandtotals(data, key_prefix=''):
    grand_total = (
        Decimal(data.get('{}{}'.format(key_prefix, 'total')))
        + Decimal(data.get('shipping_cost'))
        + Decimal(data.get('fees'))
    )
    if data.get('flat_discount_amount') and key_prefix != '':
        discounted_grand_total = grand_total - Decimal(data.get('flat_discount_amount'))
        grand_total = discounted_grand_total if discounted_grand_total > 0 else 0
    return {'{}{}'.format(key_prefix, 'grand_total'): str(grand_total)}


def get_price_with_currency(price, currency):
    if currency == DEFAULT_CURRENCY:
        return '{} {}'.format(price, currency_symbol_mapping[currency])
    return '{}{}'.format(currency_symbol_mapping[currency], price)


def create_promo_code_products(promo_code):
    Product = apps.get_model('shop', 'Product')
    PromoCodeProduct = apps.get_model('shop', 'PromoCodeProduct')

    for product in Product.objects.all():
        pcp = PromoCodeProduct()
        pcp.promo_code = promo_code
        pcp.product = product
        pcp.discount = promo_code.auto_apply_discount
        pcp.save()


def apply_discount(promo_code, eligible_products, bag):
    if promo_code.flat_discount:
        bag.update({
            'flat_discount_amount': str(promo_code.flat_discount_amount),
        })
        return bag

    PromoCodeProduct = apps.get_model('shop', 'PromoCodeProduct')
    for product in eligible_products:
        discount = PromoCodeProduct.objects.get(promo_code=promo_code, product=product).discount
        discounted_price = round(product.price_hrk - product.price_hrk * discount / 100, 2)

        bag_product = bag['products'][product.slug]
        bag_product.update({
            'discount': str(discount),
            'new_price_hrk': str(discounted_price),
            'new_subtotal': str(int(bag_product['quantity']) * discounted_price),
        })
        bag['products'][product.slug] = bag_product
    return bag


def update_bag_with_discount(bag, code, session):
    PromoCode = apps.get_model('shop', 'PromoCode')

    promo_code = PromoCode.published_objects.filter(code=code).first()
    if promo_code and promo_code.flat_discount and promo_code.flat_discount_amount < Decimal(bag.get('grand_total')):
        update_discount(bag, promo_code, session)
    else:
        clear_discount_data(bag)
        session.modified = True


def update_discount(bag, promo_code, session):
    bag_products = [product_slug for product_slug in bag.get('products')]
    discounted_products = promo_code.product_list.all()
    message = ''

    eligible_products = []
    for promo_code_product in discounted_products:
        if promo_code_product.slug in bag_products:
            eligible_products.append(promo_code_product)

    if len(eligible_products) < 1 and not promo_code.flat_discount:
        message = _('This code does not apply to items in your bag.')
        return message

    if promo_code.flat_discount and promo_code.flat_discount_amount >= Decimal(bag.get('grand_total')):
        message = _('Grand total must exceed the gift card amount.')
        return message

    if (len(eligible_products) > 0 or promo_code.flat_discount) and promo_code.code == bag.get('promo_code'):
        message = _('The code is already applied.')

    bag = apply_discount(promo_code, eligible_products, bag)
    session.modified = True

    new_total = Decimal('0.00')
    for product, data in bag['products'].items():
        if data.get('new_subtotal'):
            new_total += Decimal(data.get('new_subtotal'))
        else:
            new_total += Decimal(data.get('subtotal'))

    bag.update({
        'promo_code': promo_code.code,
        'new_total': str(new_total),
    })
    bag.update({
        **get_grandtotals(bag, key_prefix='new_'),
    })
    set_tax(bag, key_prefix='new_')
    session.modified = True

    return message


def clear_discount_data(bag):
    bag.pop('promo_code', None)
    bag.pop('new_total', None)
    bag.pop('new_grand_total', None)
    bag.pop('new_tax', None)

    for _, product in bag.get('products', {}).items():
        product.pop('discount', None)
        product.pop('new_price_hrk', None)
        product.pop('new_subtotal', None)


def create_installment_code(installment):
    if installment.installment_number < 10:
        installments = '0{}'.format(installment.installment_number)
    else:
        installments = str(installment.installment_number)
    installment.installment_code = 'Y02{}'.format(installments)
