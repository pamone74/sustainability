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
    ("US", "User"),
]

class Manufacturer(models.Model):
    MANUFACTURE_LOCATION_CHOICES = [
    ("Abu Dhabi", "Abu Dhabi"),
    ("Dubai", "Dubai"),
    ("Ajman", "Ajman"),
    ]
    product_name = models.CharField(_("Product Name"), max_length=50, default="Unknown")
    manufacturer_name = models.CharField(_("Company Name"), max_length=50,default="Unknown")
    manufacture_location = models.CharField(_("Location"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="Abu Dhabi")
    product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS, default="RC")
    product_quantity = models.IntegerField(_("Quantity"), default=0)
    product_mf_date = models.DateTimeField(_("Manufacturing Date"), auto_now=True, auto_now_add=False)
    product_expiry_date = models.DateTimeField(_("Expiry Date"), auto_now=False, auto_now_add=False,default=datetime.datetime.now)

# 
# class Products(models.Model):
    # product_id = models.CharField(_("Product ID"), max_length=50)
    # manufacturer = models.ForeignKey(Manufacturer, verbose_name=_(""), on_delete=models.CASCADE,default=1)
    # product_name = models.CharField(_("Product Name"), max_length=50, default="Unknown")
    # manufacturer_name = models.CharField(_("Company Name"), max_length=50,default="Unknown")
    # manufacture_location = models.CharField(_("Location"), max_length=50, default="Abu Dhabi")
    # # product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS, default="RC")
    # product_quantity = models.IntegerField(_("Quantity"), default=0)
    # product_mf_date = models.DateTimeField(_("Manufacturing Date"), auto_now=True, auto_now_add=False)
    # # product_expiry_date = models.DateTimeField(_("Expiry Date"), auto_now=False, auto_now_add=False,default=datetime.datetime.now)
# 
    # def save(self, *args, **kwargs):
        # if not self.product_id:
            # first_two_words = "_".join(self.product_name.split()[:2]).upper()
            # date_manufacture = self.manfacturer.product_mf_date
            # total_products = Products.objects.count() + 1
            # self.product_id = f"{first_two_words}{date_manufacture}{total_products}"
        # self.product_name = self.manufacturer.product_name
        # self.manufacturer_name = self.manufacturer.manufacturer_name
        # self.manufacture_location = self.manufacturer.manufacture_location
        # self.product_type = self.manufacturer.product_type
        # self.product_quantity = self.manufacturer.product_quantity
        # self.product_mf_date = self.manufacturer.product_mf_date
        # self.product_expiry_date = self.manufacturer.product_expiry_date
        # super().save(*args, **kwargs)
# 

class Product(models.Model):
    product_id = models.CharField(_("Product ID"), max_length=50, editable=False, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_(""), on_delete=models.CASCADE,default=1)
    product_name = models.CharField(_("Product Name"), max_length=50, default="Unknown")
    manufacturer_name = models.CharField(_("Company Name"), max_length=50,default="Unknown")
    manufacture_location = models.CharField(_("Location"), max_length=50, default="Abu Dhabi")
    product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS, default="RC")
    product_quantity = models.IntegerField(_("Quantity"), default=0)
    product_mf_date = models.DateTimeField(_("Manufacturing Date"), auto_now=True, auto_now_add=False)
    product_expiry_date = models.DateTimeField(_("Expiry Date"), auto_now=False, auto_now_add=False,default=datetime.datetime.now)
    product_ownership = models.CharField(_("Ownership"), max_length=50, choices=CHOICES_FOR_USERS, default="US")

    def save(self, *args, **kwargs):
        if not self.product_id:
            first_two_words = "_".join(self.product_name.split()[:2]).upper()
            first_w_name = "_".join(self.manufacturer_name.split()[:2]).upper()
            total_products = Product.objects.count() + 1
            self.product_id = f"{first_two_words}{first_w_name}{total_products}"
        self.product_name = self.manufacturer.product_name
        super().save(*args, **kwargs)




 


