# Generated by Django 2.2.7 on 2019-11-15 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_squashed_0009_auto_20191115_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cart',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]