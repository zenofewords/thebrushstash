# Generated by Django 2.2.7 on 2019-12-03 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thebrushstash', '0014_auto_20191203_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpagecontent',
            name='content',
            field=models.TextField(max_length=30000),
        ),
        migrations.AlterField(
            model_name='staticpagecontent',
            name='content_cro',
            field=models.TextField(max_length=30000),
        ),
    ]
