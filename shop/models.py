from django.contrib.postgres.fields import JSONField
from django.db import models

from shop.mixins import (
    ShopObjectMixin,
)
from shop.utils import (
    get_default_product_type,
    update_product_prices,
)
from thebrushstash.mixins import TimeStampMixin
from thebrushstash.models import PublishedMixin


class ExchangeRate(TimeStampMixin):
    currency = models.CharField(max_length=10)
    currency_code = models.CharField(max_length=10)
    state_iso = models.CharField(max_length=10)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=8)
    middle_rate = models.DecimalField(max_digits=10, decimal_places=8)
    selling_rate = models.DecimalField(max_digits=10, decimal_places=8)
    added_value = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='The percentage added when converting from HRK'
    )

    class Meta:
        verbose_name = 'Exchange rate'
        verbose_name_plural = 'Exchange rates'

    def __str__(self):
        return '1 {} equals {} HRK'.format(self.currency, self.middle_rate)


class Product(ShopObjectMixin, TimeStampMixin, PublishedMixin):
    product_type = models.ForeignKey(
        'shop.ProductType', default=get_default_product_type, on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to='shop/%Y/%m/', blank=True, null=True, help_text='Used in the description section'
    )
    srcsets = JSONField(blank=True, null=True)
    foreword = models.TextField(
        max_length=300, blank=True, help_text='Short decription',
    )
    new = models.BooleanField(default=True)
    in_stock = models.IntegerField(default=0)
    ordering = models.IntegerField(
        default=0, blank=True,
        help_text='If set to 0, products are ordered by "new", then by creation date'
    )
    price_hrk = models.DecimalField(
        verbose_name='Price (HRK)', max_digits=14, decimal_places=2, blank=True, null=True,
    )
    price_usd = models.DecimalField(
        verbose_name='Price (USD)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK when saved"
    )
    price_eur = models.DecimalField(
        verbose_name='Price (EUR)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK when saved"
    )
    price_gbp = models.DecimalField(
        verbose_name='Price (GBP)', max_digits=14, decimal_places=2, blank=True, null=True,
        help_text="Auto populates from HRK when saved"
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-ordering', '-new', '-created_at', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        update_product_prices(self)
        super().save(*args, **kwargs)


class ProductType(ShopObjectMixin, TimeStampMixin):
    class Meta:
        verbose_name = 'Product type'
        verbose_name_plural = 'Product types'

    def __str__(self):
        return self.name


class Invoice(TimeStampMixin):
    class InvoiceStatus:
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

    class InvoicePaymentMethod:
        ON_DELIVERY = 'on-delivery'
        PAYPAL = 'paypal'
        CREDIT_CARD = 'credit-card'

        CHOICES = (
            (ON_DELIVERY, 'Pay on delivery'),
            (PAYPAL, 'Paypal'),
            (CREDIT_CARD, 'Credit card'),
        )

    email = models.EmailField(max_length=200)
    full_name = models.CharField(max_length=500)
    country = models.ForeignKey(
        'thebrushstash.Country', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    city = models.CharField(max_length=500)
    address = models.CharField(max_length=1000)
    zip_code = models.CharField(max_length=500)
    state_county = models.CharField(max_length=500, blank=True)
    company_name = models.CharField(max_length=500, blank=True)
    company_address = models.CharField(max_length=500, blank=True)
    company_uin = models.CharField(max_length=500, blank=True)

    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    note = models.TextField(blank=True)
    payment_method = models.CharField(max_length=100, choices=InvoicePaymentMethod.CHOICES)
    status = models.CharField(max_length=100, choices=InvoiceStatus.CHOICES)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class Transaction(TimeStampMixin):
    order = models.ForeignKey('shop.Invoice', on_delete=models.deletion.CASCADE)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return 'Transaction for {}'.format(self.order)


class Showcase(ShopObjectMixin, PublishedMixin):
    class Meta:
        verbose_name = 'Showcase'
        verbose_name_plural = 'Showcases'

    def __str__(self):
        return self.name
