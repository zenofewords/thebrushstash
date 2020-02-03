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

    def __str__(self):
        return self.username


class NewsletterRecipient(models.Model):
    subscribed = models.BooleanField()
    email = models.EmailField()
    language_preference = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.deletion.CASCADE, blank=True, null=True,
    )
    token = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.language_preference = get_language()
        super().save(*args, **kwargs)
