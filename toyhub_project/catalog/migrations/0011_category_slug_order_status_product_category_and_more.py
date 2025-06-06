# Generated by Django 5.2.1 on 2025-05-25 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_product_stock_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='default-slug', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('delivering', 'Delivering'), ('received', 'Received'), ('cancelled', 'Cancelled')], default='processing', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
