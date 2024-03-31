from django.db import models
from django.utils import timezone
from django.db import transaction
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
#Amone's models
CHOICES_FOR_PRODUCTS= [
    ("RC", "Recycable"),
    ("NRC", "Non Recycable"),
    ("RU", "Reusable"),
    ("RCV", "Recover"),
]

CHOICES_FOR_USERS= [
    ("CS", "Consumer"),
    ("MF", "New Product"),
    ("MC","Merchant"),
]

TRACK_STATUS=[
    ("RC", "Recycaled"),
    ("RU", "Reusing"),
    ("RCV", "Recover"),
    ("NO", "Not Recyled"),
]
MANUFACTURE_LOCATION_CHOICES = [
("AD", "Abu Dhabi"),
("DU", "Dubai"),
("AJ", "Ajman"),
("SH", "Sharjah"),
("AL", "Al Ain"),
("FU", "Fujairah"),
("RA", "Ras Al Khaimah"),
("UM", "Umm Al Quwain"),
]



class Manufacturer(models.Model):
    product_name = models.CharField(_("Product Name"), max_length=50,default="Unknown")
    product_quantity = models.IntegerField(_("Quantity"), default=0)
    product_catgories = models.CharField(_("Catagories"), max_length=3, choices=CHOICES_FOR_PRODUCTS, default="RC")
    manufacturer_name = models.CharField(_("Company Name"), max_length=50)
    manufacture_location = models.CharField(_("Location"), max_length=50, choices=MANUFACTURE_LOCATION_CHOICES, default="Abu Dhabi")
    manufacturer_email = models.EmailField(_("Email"), max_length=50, default="")
    manufacturer_phone = models.CharField(_("Phone"), max_length=50,default="")
    manufacturer_address = models.CharField(_("Address"), max_length=50, default='Abu Dhabi')
    product_description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.product_name


class Product(models.Model):
    product_id = models.CharField(_("Product ID"), max_length=50, editable=False, unique=True)
    product_name = models.CharField(_("Product Name"), max_length=50)
    manufacturer_name = models.CharField(_("Company Name"), max_length=50)
    manufacture_location = models.CharField(_("Location"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="AD")
    product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS, default="RC")
    product_quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    product_mf_date = models.DateTimeField(_("Manufacturing Date"),default=datetime.datetime.now)
    product_expiry_date = models.DateTimeField(_("Expiry Date"), auto_now=False, auto_now_add=False,default=datetime.datetime.now)
    product_ownership = models.CharField(_("Ownership"), max_length=50, 
                                         choices=CHOICES_FOR_USERS, default="CS")


    def save(self, *args, **kwargs):
        if not self.product_id:
            first_two_words = "_".join(self.product_name.split()[:2]).upper()
            first_w_name = "_".join(self.manufacturer_name.split()[:2]).upper()
            total_products = Product.objects.count() + 1
            self.product_id = f"{first_two_words}{first_w_name}{total_products}"
        # with transaction.atomic():
            # # total_pdt = Users.objects.filter(product_name=self.product_name).aggregate(total=models.Sum('product_quantity'))['total']
            # if total_pdt is not None:
                # self.product_quantity = total_pdt
                # self.save(update_fields=['product_quantity'])
        super().save(*args, **kwargs)


class Users(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    user_name = models.CharField(_("User Name"), max_length=50)
    telephone_number = models.CharField(_("Telephone"), max_length=10)
    user_email = models.EmailField(_("Email Id"), max_length=254)
    user_catagory = models.CharField(_("Catagory"), max_length=2, choices=CHOICES_FOR_USERS, default="US")
    user_points = models.IntegerField(_("Points"), default=0)
    product_quantity = models.IntegerField(_("Quantity"), default=0)

class Ownership(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),null=True, on_delete=models.SET_NULL)
    product = models.ManyToManyField(Product, verbose_name=_("Product"), related_name="who_own_the_product")
    status = models.CharField(_("Recycle Status"), max_length=10,choices=TRACK_STATUS, default="NO")
    date = models.DateTimeField(_("Date"), auto_now=True, auto_now_add=False)
    product_quantity = models.IntegerField(_("Quantity"), default=0)

    # def save(self, *args, **kwargs):
        # with transaction.atomic():
            # self.product_quantity = self.user.product_quantity
        # super().save(*args, **kwargs)
class AddEvent(models.Model):
    event_name = models.CharField(_("Event Name"), max_length=50)
    event_date = models.DateTimeField(_("Event Date"), auto_now=False, auto_now_add=False)
    event_location = models.CharField(_("Location"), max_length=50)
    event_description = models.TextField(_("Description"), blank=True)

class ProfileUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=50)
    phone = models.CharField(_("Phone"), max_length=10)
    full_name = models.CharField(_("Full Name"), max_length=50, null=False, blank=False, default="")
    city = models.CharField(_("City"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="AD")
    country = models.CharField(_("Country"), max_length=50)
    country_origin = models.CharField(_("Country Origin"), max_length=50, default="UAE")
    date_created = models.DateTimeField(_("Date Created"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, auto_now_add=False)
    email =     models.EmailField(_("email"), max_length=20, default="")

    def __str__(self):
        return self.user.username