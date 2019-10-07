from django.apps import apps

defaultProductType = 'brush'


def get_default_product_type():
    ProductType = apps.get_model('shop', 'ProductType')

    try:
        return ProductType.objects.get(slug=defaultProductType).pk
    except ProductType.DoesNotExist:
        return None


def update_product_prices(product):
    ExchangeRate = apps.get_model('shop', 'ExchangeRate')
    exchange_rates = ExchangeRate.objects.all()

    if product.price_hrk and exchange_rates.count() > 0:
        price = product.price_hrk

        for er in exchange_rates:
            setattr(product, 'price_{}'.format(er.currency.lower()), price / er.middle_rate)
