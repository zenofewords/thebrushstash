from django.db import models


class ShopObjectMixin(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(
        max_length=500, blank=True, help_text='If left empty, auto populates from name'
    )
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
