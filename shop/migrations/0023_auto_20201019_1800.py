# Generated by Django 3.1.2 on 2020-10-19 17:00

from django.db import migrations, models
import django.db.models.deletion


def copy_price_to_old_price(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')

    for product in Product.objects.all():
        product.old_price_hrk = product.price_hrk
        product.old_price_usd = product.price_usd
        product.old_price_gbp = product.price_gbp
        product.old_price_eur = product.price_eur
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20200823_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('label_cro', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Custom label',
                'verbose_name_plural': 'Custom labels',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='free_shipping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price_eur',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Auto populates from HRK when saved', max_digits=14, null=True, verbose_name='Old price (EUR)'),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price_gbp',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Auto populates from HRK when saved', max_digits=14, null=True, verbose_name='Old price (GBP)'),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price_hrk',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True, verbose_name='Old price (HRK)'),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price_usd',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Auto populates from HRK when saved', max_digits=14, null=True, verbose_name='Old price (USD)'),
        ),
        migrations.AddField(
            model_name='product',
            name='custom_label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customlabel'),
        ),
        migrations.RunPython(
            code=copy_price_to_old_price,
            reverse_code=migrations.operations.special.RunPython.noop,
        ),
    ]
