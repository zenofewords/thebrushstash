from django.db import models
from django.utils.translation import get_language

from thebrushstash.mixins import (
    LinkedMixin,
    PublishedMixin,
    TimeStampMixin,
)


class Country(PublishedMixin):
    name = models.CharField(max_length=500)
    name_cro = models.CharField(max_length=500, blank=True)
    slug = models.CharField(max_length=500)
    shipping_cost = models.DecimalField(
        verbose_name='Shipping cost', max_digits=14, decimal_places=2, blank=False, null=True,
    )

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('slug', )

    def __str__(self):
        language = get_language()
        if language == 'hr':
            return self.name_cro
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
    name_cro = models.CharField(max_length=500, blank=True)


class FooterShareLink(LinkedMixin, PublishedMixin):
    name_cro = models.CharField(max_length=500, blank=True)


class Region(PublishedMixin):
    name = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    ordering = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        ordering = ('-ordering', )

    def __str__(self):
        return self.name


class StaticPageContent(models.Model):
    title = models.CharField(max_length=1000)
    title_cro = models.CharField(max_length=1000)
    slug = models.CharField(max_length=100)
    content = models.TextField(max_length=30000)
    content_cro = models.TextField(max_length=30000)

    class Meta:
        verbose_name = 'Static page content'
        verbose_name = 'Static pages content'

    def __str__(self):
        return self.title


class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return '{} - {}'.format(self.name, self.value)


class QandAPair(models.Model):
    question = models.TextField(max_length=2000)
    question_cro = models.TextField(max_length=2000)
    answer = models.TextField(max_length=5000)
    answer_cro = models.TextField(max_length=5000)
    ordering = models.IntegerField(
        default=0, blank=True,
        help_text='If set to 0, items are ordered by creation date'
    )

    class Meta:
        verbose_name = 'Question and answer pair'
        verbose_name = 'Question and answer pair'
        ordering = ('-ordering', )

    def __str__(self):
        return self.question[:50]
