import operator
from decimal import Decimal

from django.apps import apps

from shop.constants import (
    FREE_SHIPPING_PRICE,
    FREE_SHIPPING_PRODUCTS,
    TAX,
)
from thebrushstash.constants import (
    DEFAULT_COUNTRY,
    DEFAULT_CURRENCY,
    DEFAULT_REGION,
    currency_symbol_mapping,
)
from thebrushstash.models import (
    Country,
    ExchangeRate,
    Region,
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


def update_product_rating(product, score):
    product.ratings += 1
    product.score += score
    product.save()


def set_shipping_cost(bag, region, country_name=None):
    quantity_condition = int(bag.get('total_quantity', 0)) >= int(FREE_SHIPPING_PRODUCTS)
    cost_condition = Decimal(bag.get('total', 0)) >= Decimal(FREE_SHIPPING_PRICE)
    free_shipping = (quantity_condition or cost_condition) and country_name == DEFAULT_COUNTRY

    cost = 0
    if country_name:
        country = Country.published_objects.filter(name=country_name).first()
        cost = country.shipping_cost if country and country.shipping_cost else cost

    shipping_cost = Decimal('0.00') if free_shipping else Decimal(cost)
    bag['shipping_cost'] = str(shipping_cost)
    bag['grand_total'] = str(Decimal(bag.get('total', 0)) + shipping_cost)


def set_tax(bag):
    total = Decimal(bag.get('total', 0))
    bag['tax'] = str(round(total - total / (Decimal(TAX) + 1), 2))


def get_totals(data, key, operator, product={}, quantity=None):
    quantity = quantity if quantity else data.get('quantity')

    price_hrk = Decimal(data.get('price_hrk'))
    subototal = quantity * price_hrk
    prices = {'price_hrk': str(price_hrk)} if key == 'subtotal' else {}

    if product:
        return {'{}'.format(key): str(operator(Decimal(product.get('{}'.format(key))), subototal))}
    else:
        return {
            '{}'.format(key): str(subototal),
            **prices,  # noqa
        }


def get_grandtotals(data):
    return {'grand_total': str(Decimal(data.get('total')) + Decimal(data.get('shipping_cost')))}


def format_price_with_currency(price, currency):
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


def apply_discount(code, eligible_products, bag):
    PromoCodeProduct = apps.get_model('shop', 'PromoCodeProduct')

    for product in eligible_products:
        discount = PromoCodeProduct.objects.get(promo_code__code=code, product=product).discount
        discounted_price = round(product.price_hrk - product.price_hrk * discount / 100, 2)

        bag_product = bag['products'][product.slug]
        bag_product.update({
            'discount': str(discount),
            'price_hrk': str(discounted_price),
            'subtotal': str(int(bag_product['quantity']) * discounted_price),
        })
        bag['products'][product.slug] = bag_product
    return bag
