# Generated by Django 2.2.9 on 2020-02-03 07:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0012_auto_20191222_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('schedule_at', models.DateTimeField(blank=True)),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='shop/%Y/%m/')),
                ('body_image', models.ImageField(blank=True, null=True, upload_to='shop/%Y/%m/')),
                ('header_text_cro', models.TextField(blank=True)),
                ('header_text', models.TextField(blank=True)),
                ('body_text_cro', models.TextField(blank=True)),
                ('body_text', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('ready', 'Ready'), ('in progress', 'In Progress'), ('finished', 'Finished'), ('failed', 'Failed')], max_length=100)),
                ('status_message', models.TextField(blank=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('recipient_list', models.ManyToManyField(help_text='Use for testing, if left blank the newsletter will be sent to all recipients.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletter',
                'ordering': ('-created_at',),
            },
        ),
    ]
