from django.db import models


class ShopObjectMixin(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
