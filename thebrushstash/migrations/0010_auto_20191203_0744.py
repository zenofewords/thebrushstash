# Generated by Django 2.2.7 on 2019-12-03 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thebrushstash', '0009_qandapair'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticpagecontent',
            name='content_cro',
            field=models.TextField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staticpagecontent',
            name='title_cro',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staticpagecontent',
            name='content',
            field=models.TextField(max_length=2000),
        ),
    ]
