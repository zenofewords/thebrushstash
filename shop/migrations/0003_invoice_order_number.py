# Generated by Django 2.2.7 on 2019-11-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_invoice_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='order_number',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
