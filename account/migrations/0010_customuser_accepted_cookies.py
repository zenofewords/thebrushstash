# Generated by Django 3.1 on 2020-08-05 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200805_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='accepted_cookies',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
