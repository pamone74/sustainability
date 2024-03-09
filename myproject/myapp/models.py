from django.db import models
from django.utils import timezone
# this is for the page translation
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import datetime

'''
There will be five modoles for this projects: 
1. Administrator | or the Authorized personel for tracking the records 
2. The Producers or the Factories producing the products, custom import
3. Marchants | wholesalers 
4. users | retail outlets 
5. Products 

    The administrators will have the columns for the product_id, product_img, 
product_ownership, product_quantity, product_origin, product_type,product_name, 
        ->  The product_id is the unique ID that will be assigned to the product 
during manufacturing
        -> The rest  of the parts are explained in the codes

'''
CHOICES_FOR_PRODUCTS= [
    ("RC", "Recycable"),
    ("NRC", "Non Recycable"),
]

CHOICES_FOR_USERS= [
    ("MC", "Merchant"),
    ("CN", "Consumer"),
]

class Products(models.Model):
    product_id = models.CharField(_("Product ID"), max_length=50)
    product_quantity = models.IntegerField(_("Product Quantity"))
    product_name = models.CharField(_("Product Name"), max_length=15)
    product_manufacture_date = models.DateTimeField(_("Date of Manufacture"), auto_now=False, auto_now_add=False)
    product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS)

    def save(self, *args, **kwargs):
        if not self.product_id:
            first_two_words = "_".join(self.product_name.split()[:2]).upper()
            date_manufacture = self.product_manufacture_date.day
            total_products = Products.objects.count() + 1
            self.product_id = f"{first_two_words}{date_manufacture}{total_products}"
        super().save(*args, **kwargs)

class Manufacturer(models.Model):
    manufacturer_name = models.CharField(_("Name"), max_length=50,default="Unknown")
    MANUFACTURE_LOCATION_CHOICES = [
        ("Abu Dhabi", "Abu Dhabi"),
        ("Dubai", "Dubai"),
        ("Ajman", "Ajman"),
    ]
    manufacture_location = models.CharField(_("Location"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="Abu Dhabi")
    products_details = models.ForeignKey(Products, verbose_name=_("Products details"), on_delete=models.CASCADE)
    product_quantity = models.IntegerField(_("Quantity"), default=0)

