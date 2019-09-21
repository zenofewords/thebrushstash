from django.db import models


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ShopObjectMixin(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
