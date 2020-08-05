from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

from shop.mixins import ShopObjectMixin
from shop.utils import (
    create_promo_code_products,
    get_default_product_type,
    update_product_prices,
    update_product_rating,
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
    score = models.PositiveIntegerField(default=0)
    ratings = models.PositiveIntegerField(default=0)

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

    title_cro = models.CharField(max_length=500, blank=True)
    foreword_cro = models.TextField(max_length=300, blank=True)
    description_cro = models.TextField(blank=True)

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
    PROCESSED = 'processed'
    PACKAGED = 'packaged'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    CHOICES = (
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (PROCESSED, 'Processed'),
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
    phone_number = models.CharField(max_length=500, blank=True)
    company_name = models.CharField(max_length=500, blank=True)
    company_address = models.CharField(max_length=500, blank=True)
    company_uin = models.CharField(max_length=500, blank=True)

    order_number = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )

    order_total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    cart = models.TextField(blank=True)
    note = models.TextField(blank=True)
    payment_method = models.CharField(
        max_length=100, choices=InvoicePaymentMethod.CHOICES, blank=True
    )
    region = models.ForeignKey(
        'thebrushstash.Region', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    promo_code = models.ForeignKey(
        'shop.PromoCode', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    status = models.CharField(max_length=100, choices=InvoiceStatus.CHOICES)

    shipping_first_name = models.CharField(max_length=500, blank=True)
    shipping_last_name = models.CharField(max_length=500, blank=True)
    invoice_shipping_country = models.ForeignKey(
        'thebrushstash.Country', on_delete=models.deletion.CASCADE, blank=True, null=True,
        related_name='invoice_shipping_country',
    )
    shipping_city = models.CharField(max_length=500, blank=True)
    shipping_address = models.CharField(max_length=1000, blank=True)
    shipping_zip_code = models.CharField(max_length=500, blank=True)
    shipping_state_county = models.CharField(max_length=500, blank=True)

    installments = models.IntegerField(default=0, blank=True, null=True)

    resend_purchase_confirmation_email = models.BooleanField(default=False)
    bag_dump = models.JSONField(blank=True, null=True)
    register_user = models.BooleanField(default=False)
    subscribe_to_newsletter = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class InvoiceItem(TimeStampMixin):
    invoice = models.ForeignKey('shop.Invoice', on_delete=models.deletion.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.deletion.CASCADE)
    promo_code = models.ForeignKey(
        'shop.PromoCode', on_delete=models.deletion.CASCADE, blank=True, null=True
    )
    sold_count = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


class Showcase(ShopObjectMixin, PublishedMixin):
    name_cro = models.CharField(max_length=500, blank=True)
    description_cro = models.TextField(blank=True)

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
    show_in_gallery = models.BooleanField(
        default=True, help_text='Unchecking will hide the image for galleries (detail page)'
    )
    standalone = models.BooleanField(
        default=False, help_text='Automatically set for the "one item per gallery" use case'
    )
    srcsets = models.JSONField(blank=True, null=True)
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


class EmailSource:
    REGISTRATION = 'registration'
    NEWSLETTER = 'newsletter'
    PURCHASE = 'purchase'

    CHOICES = (
        (REGISTRATION, 'Registration'),
        (NEWSLETTER, 'Newsletter'),
        (PURCHASE, 'Purchase'),
    )


class EmailAuditStatus:
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'

    CHOICES = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
        (FAILED, 'Failed'),
    )


class EmailAudit(TimeStampMixin):
    sent_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100, choices=EmailSource.CHOICES)
    status = models.CharField(max_length=100, choices=EmailAuditStatus.CHOICES)
    receiver = models.CharField(max_length=500)
    payment_method = models.CharField(max_length=100, choices=InvoicePaymentMethod.CHOICES)
    content = models.TextField()
    error_message = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Email audit'
        verbose_name_plural = 'Email audits'
        ordering = ('status', '-created_at', )

    def __str__(self):
        return '{} by {}'.format(self.receiver, self.payment_method)


class Review(TimeStampMixin, PublishedMixin):
    product = models.ForeignKey('shop.Product', on_delete=models.deletion.CASCADE)
    user = models.ForeignKey('account.CustomUser', on_delete=models.deletion.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-created_at', )

    def __str__(self):
        return '{} review by {}'.format(self.product.name, self.user.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_product_rating(self.product, self.score)


class NewsletterStatus:
    READY = 'ready'
    IN_PROGRESS = 'in progress'
    FINISHED = 'finished'
    FAILED = 'failed'

    CHOICES = (
        (READY, 'Ready'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (FAILED, 'Failed'),
    )


class Newsletter(TimeStampMixin, PublishedMixin):
    schedule_at = models.DateTimeField(blank=True)
    recipient_list = models.ManyToManyField(
        'account.NewsletterRecipient',
        help_text='Use for testing, if left blank the newsletter will be sent to all recipients.',
        blank=True
    )
    header_image = models.ImageField(upload_to='newsletter/%Y/%m/', blank=True, null=True)
    body_image = models.ImageField(upload_to='newsletter/%Y/%m/', blank=True, null=True)

    title_cro = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    header_text_cro = models.TextField(blank=True)
    header_text = models.TextField(blank=True)
    body_text_cro = models.TextField(blank=True)
    body_text = models.TextField(blank=True)

    status = models.CharField(max_length=100, choices=NewsletterStatus.CHOICES, blank=True)
    status_message = models.TextField(blank=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletter'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.schedule_at and not self.status:
            self.status = NewsletterStatus.READY
            self.status_message = 'Scheduled for delivery'
        super().save(*args, **kwargs)


class PromoCode(TimeStampMixin, PublishedMixin):
    code = models.CharField(max_length=50, unique=True)
    expires = models.DateTimeField(
        blank=True, null=True, help_text='The code will become inactive on the set time and date.'
    )
    single_use = models.BooleanField(
        default=False, help_text='Check if the code is intended for one use only.'
    )
    auto_apply_discount = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True,
        help_text='Input to apply the same discount to all products.'
    )
    product_list = models.ManyToManyField(
        'shop.Product', blank=True, through='PromoCodeProduct',
        help_text='If blank, creates a discount template for every product.'
    )

    class Meta:
        verbose_name = 'Promo code'
        verbose_name_plural = 'Promo codes'
        ordering = ('-created_at', )

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.pk is None and self.auto_apply_discount:
            super().save(*args, **kwargs)
            create_promo_code_products(self)
        else:
            super().save(*args, **kwargs)


class PromoCodeProduct(TimeStampMixin):
    promo_code = models.ForeignKey('shop.PromoCode', on_delete=models.deletion.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.deletion.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Promo code for product'
        verbose_name_plural = 'Promo code for products'
        unique_together = ['promo_code', 'product']

    def __str__(self):
        return '{}, {}, {}'.format(self.promo_code, self.product, self.discount)
