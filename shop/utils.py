from django.apps import apps

defaultProductType = 'brush'


def get_default_prodcut_type():
    ProductType = apps.get_model('shop', 'ProductType')
    return ProductType.objects.get(slug=defaultProductType).pk


def update_prices_for_product(product):
    ExchangeRate = apps.get_model('shop', 'ExchangeRate')
    exchage_rates = ExchangeRate.objects.all()

    if product.price_hrk and exchage_rates.count() > 0:
        price = product.price_hrk

        for exr in exchage_rates:
            setattr(product, 'price_{}'.format(exr.currency.lower()), price / exr.middle_rate)
