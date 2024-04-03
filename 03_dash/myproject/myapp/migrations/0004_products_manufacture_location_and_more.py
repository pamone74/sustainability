# Generated by Django 5.0.2 on 2024-03-17 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_remove_manufacturer_products_details_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="manufacture_location",
            field=models.CharField(
                default="Abu Dhabi", max_length=50, verbose_name="Location"
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="manufacturer_name",
            field=models.CharField(
                default="Unknown", max_length=50, verbose_name="Company Name"
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="product_expiry_date",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Expiry Date"
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="product_mf_date",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Manufacturing Date"
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="product_name",
            field=models.CharField(
                default="Unknown", max_length=50, verbose_name="Product Name"
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="product_quantity",
            field=models.IntegerField(default=0, verbose_name="Quantity"),
        ),
        migrations.AddField(
            model_name="products",
            name="product_type",
            field=models.CharField(
                choices=[("RC", "Recycable"), ("NRC", "Non Recycable")],
                default="RC",
                max_length=50,
                verbose_name="Product Type",
            ),
        ),
    ]
