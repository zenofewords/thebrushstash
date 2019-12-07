# Generated by Django 2.2.8 on 2019-12-07 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thebrushstash', '0016_country_region'),
        ('account', '0004_newsletterrecipient_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_shipping_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_shipping_country', to='thebrushstash.Country'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_city',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_first_name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_last_name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_state_county',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shipping_zip_code',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
