from decimal import Decimal

from django.apps import apps

from shop.constants import (
    FREE_SHIPPING_PRICE,
    FREE_SHIPPING_PRODUCTS,
    TAX,
)
from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.models import (
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


def set_shipping_cost(bag, current_region):
    quantity_condition = int(bag.get('total_quantity', 0)) >= int(FREE_SHIPPING_PRODUCTS)
    cost_condition = Decimal(bag.get('total_hrk', 0)) >= Decimal(FREE_SHIPPING_PRICE)
    free_shipping = quantity_condition or cost_condition

    for region in Region.published_objects.all():
        cost = Decimal('0.00') if free_shipping else region.shipping_cost
        bag['shipping_cost_{}'.format(region.currency)] = str(cost)

    if current_region != DEFAULT_REGION and not free_shipping:
        region = Region.published_objects.get(name=current_region)
        exchange_rate = ExchangeRate.objects.get(currency__iexact=region.currency)

        bag['shipping_cost_hrk'] = str(round(region.shipping_cost * exchange_rate.middle_rate, 2))
    bag['grand_total_hrk'] = str(
        Decimal(bag['total_hrk']) + Decimal(bag['shipping_cost_hrk'])
    )


def set_tax(bag, current_currency):
    bag['tax'] = str(round(Decimal(bag['total_{}'.format(current_currency)]) * Decimal(TAX), 2))


def get_totals(data, key, operator, product={}):
    quantity = data.get('quantity')

    price_hrk = Decimal(data.get('price_hrk'))
    price_eur = Decimal(data.get('price_eur'))
    price_gbp = Decimal(data.get('price_gbp'))
    price_usd = Decimal(data.get('price_usd'))
    subtotal_hrk = quantity * price_hrk
    subtotal_eur = quantity * price_eur
    subtotal_gbp = quantity * price_gbp
    subtotal_usd = quantity * price_usd
    prices = {
        'price_hrk': str(price_hrk),
        'price_eur': str(price_eur),
        'price_gbp': str(price_gbp),
        'price_usd': str(price_usd),
    } if key == 'subtotal' else {}

    if product:
        return {
            '{}_hrk'.format(key): str(
                operator(Decimal(product.get('{}_hrk'.format(key))), subtotal_hrk)
            ),
            '{}_eur'.format(key): str(
                operator(Decimal(product.get('{}_eur'.format(key))), subtotal_eur)
            ),
            '{}_gbp'.format(key): str(
                operator(Decimal(product.get('{}_gbp'.format(key))), subtotal_gbp)
            ),
            '{}_usd'.format(key): str(
                operator(Decimal(product.get('{}_usd'.format(key))), subtotal_usd)
            ),
        }
    else:
        return {
            '{}_hrk'.format(key): str(subtotal_hrk),
            '{}_eur'.format(key): str(subtotal_eur),
            '{}_gbp'.format(key): str(subtotal_gbp),
            '{}_usd'.format(key): str(subtotal_usd),
            **prices,  # noqa
        }


def get_grandtotals(data):
    return {
        'grand_total_hrk': str(
            Decimal(data.get('total_hrk')) + Decimal(data.get('shipping_cost_hrk'))
        ),
        'grand_total_eur': str(
            Decimal(data.get('total_eur')) + Decimal(data.get('shipping_cost_eur'))
        ),
        'grand_total_gbp': str(
            Decimal(data.get('total_gbp')) + Decimal(data.get('shipping_cost_gbp'))
        ),
        'grand_total_usd': str(
            Decimal(data.get('total_usd')) + Decimal(data.get('shipping_cost_usd'))
        ),
    }
