# Generated by Django 2.2.7 on 2019-11-09 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('thebrushstash', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thebrushstash.Country'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
    ]
