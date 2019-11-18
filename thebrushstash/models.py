from django.db import models

from thebrushstash.mixins import (
    LinkedMixin,
    PublishedMixin,
    TimeStampMixin,
)


class Country(PublishedMixin):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('slug', )

    def __str__(self):
        return self.name


class ExchangeRate(TimeStampMixin):
    currency = models.CharField(max_length=10)
    currency_code = models.CharField(max_length=10)
    state_iso = models.CharField(max_length=10)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=8)
    middle_rate = models.DecimalField(max_digits=10, decimal_places=8)
    selling_rate = models.DecimalField(max_digits=10, decimal_places=8)
    added_value = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='The percentage added when converting from HRK'
    )

    class Meta:
        verbose_name = 'Exchange rate'
        verbose_name_plural = 'Exchange rates'

    def __str__(self):
        return '1 {} equals {} HRK'.format(self.currency, self.middle_rate)


class TestImage(PublishedMixin):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class CreditCardLogo(LinkedMixin, PublishedMixin):
    pass


class NavigationItem(LinkedMixin, PublishedMixin):
    name_cro = models.CharField(max_length=500, blank=True)


class FooterItem(LinkedMixin, PublishedMixin):
    pass


class FooterShareLink(LinkedMixin, PublishedMixin):
    pass
