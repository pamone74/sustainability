# Generated by Django 5.0.2 on 2024-03-17 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_products_manufacture_location_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Products",
            new_name="Product",
        ),
    ]
