from django.apps import apps

from shop.constants import FREE_SHIPPING_PRODUCTS

defaultProductType = 'brush'


def get_default_product_type():
    ProductType = apps.get_model('shop', 'ProductType')

    try:
        return ProductType.objects.get(slug=defaultProductType).pk
    except ProductType.DoesNotExist:
        return None


def update_product_prices(product):
    ExchangeRate = apps.get_model('thebrushstash', 'ExchangeRate')
    exchange_rates = ExchangeRate.objects.all()

    if product.price_hrk:
        for er in exchange_rates:
            price = product.price_hrk + product.price_hrk * er.added_value / 100
            setattr(product, 'price_{}'.format(er.currency.lower()), price / er.middle_rate)


def get_shipping_cost(shipping_cost, bag):
    return 0 if int(bag.get('total_quantity', 0)) >= FREE_SHIPPING_PRODUCTS else shipping_cost
