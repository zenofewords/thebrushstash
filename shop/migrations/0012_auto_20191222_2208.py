# Generated by Django 2.2.8 on 2019-12-22 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20191218_2031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-created_at',), 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
    ]
