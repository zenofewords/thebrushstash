from webptools import webplib

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import Product
from thebrushstash.models import (
    CreditCardLogo,
    OtherImage,
)


@receiver(post_save, sender=CreditCardLogo)
@receiver(post_save, sender=OtherImage)
@receiver(post_save, sender=Product)
def create_webp_image(sender, instance, created, **kwargs):
    image_url = instance.image.url

    if image_url:
        name_without_extension = image_url.split('.')[:-1]
        webp_image_url = '{}.webp'.format('.'.join(name_without_extension))

        if instance.webp_image_url != webp_image_url:
            webplib.cwebp(
                '{}{}'.format(settings.BASE_DIR, image_url),
                '{}{}'.format(settings.BASE_DIR, webp_image_url),
                '-q 60'
            )
            instance.webp_image_url = webp_image_url
            instance.save()
