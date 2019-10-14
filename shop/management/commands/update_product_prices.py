from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Update all product prices which are in USD/EUR/GBP.'

    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.save()
