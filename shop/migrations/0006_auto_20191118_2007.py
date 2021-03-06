# Generated by Django 2.2.7 on 2019-11-18 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_invoice_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_cro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='foreword_cro',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='product',
            name='title_cro',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='showcase',
            name='description_cro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='showcase',
            name='name_cro',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
