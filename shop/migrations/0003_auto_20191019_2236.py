# Generated by Django 2.2.6 on 2019-10-19 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191019_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryitem',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='TestImage',
        ),
        migrations.DeleteModel(
            name='GalleryItem',
        ),
    ]