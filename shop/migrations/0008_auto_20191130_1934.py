# Generated by Django 2.2.7 on 2019-11-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_invoiceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryitem',
            name='show_in_gallery',
            field=models.BooleanField(default=True, help_text='Unchecking will hide the image for galleries (detail page)'),
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='standalone',
            field=models.BooleanField(default=False, help_text='Automatically set for the "one item per gallery" use case'),
        ),
    ]
