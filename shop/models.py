from django.db import models

from shop.mixins import (
    ShopObjectMixin,
    TimeStampMixin,
)
from shop.utils import (
    get_default_prodcut_type,
    update_prices_for_product,
)


class Country(models.Model):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ('slug', )

    def __str__(self):
        return self.name


class ExchangeRate(TimeStampMixin):
    currency = models.CharField(max_length=10)
    currency_code = models.CharField(max_length=10)
    state_iso = models.CharField(max_length=10)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=8)
    middle_rate = models.DecimalField(max_digits=10, decimal_places=8)
    selling_rate = models.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        verbose_name = 'Exchange rate'
        verbose_name_plural = 'Exchange rates'

    def __str__(self):
        return '1 {} equals {} HRK'.format(self.currency, self.middle_rate)


class Product(ShopObjectMixin, TimeStampMixin):
    price_hrk = models.DecimalField(
        verbose_name='Price (HRK)', max_digits=14, decimal_places=2, blank=True, null=True,
    )
    price_usd = models.DecimalField(
        verbose_name='Price (USD)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK price on save."
    )
    price_eur = models.DecimalField(
        verbose_name='Price (EUR)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK price on save."
    )
    price_chf = models.DecimalField(
        verbose_name='Price (CHF)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK price on save."
    )
    product_type = models.ForeignKey(
        'shop.ProductType', default=get_default_prodcut_type, on_delete=models.deletion.CASCADE)
    image = models.ImageField(upload_to='%Y/%m/%d/')
    ordering = models.IntegerField(default=0, blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('-ordering', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        update_prices_for_product(self)
        super().save(*args, **kwargs)


class ProductType(ShopObjectMixin, TimeStampMixin):
    class Meta:
        verbose_name = "Product type"
        verbose_name_plural = "Product types"

    def __str__(self):
        return self.name


class Order(TimeStampMixin):
    class OrderStatus:
        PENDING = 'pending'
        PACKAGED = 'packaged'
        SHIPPED = 'shipped'
        COMPLETED = 'completed'
        CANCELLED = 'cancelled'

        CHOICES = (
            (PENDING, 'Pending'),
            (PACKAGED, 'Packaged'),
            (SHIPPED, 'Shipped'),
            (COMPLETED, 'Completed'),
            (CANCELLED, 'Cancelled'),
        )

    product = models.ForeignKey('shop.Product', on_delete=models.deletion.CASCADE)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    country = models.ForeignKey('shop.Country', on_delete=models.deletion.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_postal = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500, blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(
        max_length=100, choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return '{} by {} {}'.format(self.product, self.first_name, self.last_name)


class Transaction(TimeStampMixin):
    order = models.ForeignKey('shop.Order', on_delete=models.deletion.CASCADE)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return 'Transaction for {}'.format(self.order)
