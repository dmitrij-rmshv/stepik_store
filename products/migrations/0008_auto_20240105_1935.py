# Generated by Django 3.2.18 on 2024-01-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20240105_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stripe_product_id',
        ),
        migrations.AlterField(
            model_name='product',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='stripe_price.id'),
        ),
    ]
