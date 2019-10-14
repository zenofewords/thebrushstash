from django.db import models


class LinkedMixin(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500, blank=True, default='')
    ordering = models.IntegerField(default=0, blank=True)
    external = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ('-ordering', )

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class PublishedMixin(models.Model):
    published = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        abstract = True


class WebpFieldMixin(models.Model):
    webp_image_url = models.CharField(max_length=1000, blank=True)

    class Meta:
        abstract = True
