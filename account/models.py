from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import get_language


class CustomUser(AbstractUser):
    country = models.ForeignKey(
        'thebrushstash.Country', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    city = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=1000, blank=True)
    state_county = models.CharField(max_length=500, blank=True)
    zip_code = models.CharField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=500, blank=True)
    company_name = models.CharField(max_length=500, blank=True)
    company_address = models.CharField(max_length=500, blank=True)
    company_uin = models.CharField(max_length=500, blank=True)

    shipping_first_name = models.CharField(max_length=500, blank=True)
    shipping_last_name = models.CharField(max_length=500, blank=True)
    account_shipping_country = models.ForeignKey(
        'thebrushstash.Country', on_delete=models.deletion.CASCADE, blank=True, null=True,
        related_name='account_shipping_country',
    )
    shipping_city = models.CharField(max_length=500, blank=True)
    shipping_address = models.CharField(max_length=1000, blank=True)
    shipping_zip_code = models.CharField(max_length=500, blank=True)
    shipping_state_county = models.CharField(max_length=500, blank=True)

    accepted_cookies = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.username


class LanguagePreference:
    ENGLISH = 'en'
    CROATIAN = 'hr'

    CHOICES = (
        (ENGLISH, 'English'),
        (CROATIAN, 'Croatian'),
    )


class NewsletterRecipient(models.Model):
    subscribed = models.BooleanField()
    email = models.EmailField()
    language_preference = models.CharField(
        max_length=10, choices=LanguagePreference.CHOICES, blank=True
    )
    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    token = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.language_preference:
            self.language_preference = get_language()
        super().save(*args, **kwargs)
