# Generated by Django 3.2.18 on 2024-02-22 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-id',), 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
    ]
