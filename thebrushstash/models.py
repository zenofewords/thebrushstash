from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models

from thebrushstash.mixins import (
    LinkedMixin,
    PublishedMixin,
    TimeStampMixin,
)
limit = models.Q(app_label='shop', model='product') | models.Q(app_label='shop', model='showcase')


class Country(PublishedMixin):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('slug', )

    def __str__(self):
        return self.name


class CreditCardLogo(LinkedMixin, PublishedMixin):
    pass


class CreditCardSecureLogo(LinkedMixin, PublishedMixin):
    pass


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
        ContentType, on_delete=models.CASCADE, limit_choices_to=limit,
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


class NavigationItem(LinkedMixin, PublishedMixin):
    pass


class FooterItem(LinkedMixin, PublishedMixin):
    pass


class FooterShareLink(LinkedMixin, PublishedMixin):
    pass


class TestImage(PublishedMixin):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
