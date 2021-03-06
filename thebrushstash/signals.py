from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import GalleryItem
from thebrushstash.utils import create_image_variations


@receiver(post_save, sender=GalleryItem)
def gallery_post_save_receiver(sender, instance, created, **kwargs):
    create_image_variations(instance, created)
