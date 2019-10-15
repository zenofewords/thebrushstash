from django.db import models

from thebrushstash.mixins import (
    LinkedMixin,
    PublishedMixin,
    WebpFieldMixin,
)


class Country(PublishedMixin):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ('slug', )

    def __str__(self):
        return self.name


class CreditCardSecureLogo(LinkedMixin, PublishedMixin, WebpFieldMixin):
    image = models.ImageField(upload_to='credit_card_logos')


class CreditCardLogo(LinkedMixin, PublishedMixin, WebpFieldMixin):
    image = models.ImageField(upload_to='credit_card_logos')


class NavigationItem(LinkedMixin, PublishedMixin):
    pass


class FooterItem(LinkedMixin, PublishedMixin):
    pass


class FooterShareLink(LinkedMixin, PublishedMixin):
    pass


class OtherImage(WebpFieldMixin):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='other')

    def __str__(self):
        return self.name
