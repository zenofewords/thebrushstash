from django.core.management.base import BaseCommand

from shop.models import Product
from shop.utils import update_product_prices


class Command(BaseCommand):
    help = 'Update all product prices which are in USD/EUR/GBP.'

    def _update_prices(self):
        for product in Product.objects.all():
            update_product_prices(product)

    def handle(self, *args, **options):
        self._update_prices()
