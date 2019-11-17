from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

LIMIT = models.Q(app_label='shop', model='product') | models.Q(app_label='shop', model='showcase')


class Product(ShopObjectMixin, TimeStampMixin, PublishedMixin):
    product_type = models.ForeignKey(
        'shop.ProductType', default=get_default_product_type, on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=500, blank=True)
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


class InvoiceStatus:
    PENDING = 'pending'
    PAID = 'paid'
    PACKAGED = 'packaged'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    CHOICES = (
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (PACKAGED, 'Packaged'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    )


class InvoicePaymentMethod:
    CASH_ON_DELIVERY = 'cash-on-delivery'
    PAYPAL = 'paypal'
    CREDIT_CARD = 'credit-card'

    CHOICES = (
        (CASH_ON_DELIVERY, 'Cash on delivery'),
        (PAYPAL, 'Paypal'),
        (CREDIT_CARD, 'Credit card'),
    )


class Invoice(TimeStampMixin):
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
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

    order_number = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    cart = models.TextField(blank=True)
    note = models.TextField(blank=True)
    payment_method = models.CharField(
        max_length=100, choices=InvoicePaymentMethod.CHOICES, blank=True
    )
    status = models.CharField(max_length=100, choices=InvoiceStatus.CHOICES)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class Showcase(ShopObjectMixin, PublishedMixin):

    class Meta:
        verbose_name = 'Showcase'
        verbose_name_plural = 'Showcases'

    def __str__(self):
        return self.name


class GalleryItem(TimeStampMixin):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='shop/%Y/%m/', blank=True, null=True)
    youtube_video_id = models.CharField(max_length=500, blank=True)
    ordering = models.IntegerField(
        default=0, blank=True,
        help_text='If set to 0, items are ordered by creation date'
    )
    standalone = models.BooleanField(default=False)
    srcsets = JSONField(blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=LIMIT,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Gallery item'
        verbose_name_plural = 'Gallery items'
        ordering = ('-ordering', 'created_at', )

    def __str__(self):
        description = ''

        if self.image and self.youtube_video_id:
            description = 'Youtube video with cover image'
        elif self.image:
            description = 'Image'
        elif self.youtube_video_id:
            description = 'Youtube video'
        else:
            description = 'No media attached'

        return '{} ({})'.format(self.name, description)
