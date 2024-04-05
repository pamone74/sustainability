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

COUNTRIES = [
    ("UAE", "United Arab Emirates"),
    ("USA", "United States of America"),
    ("UK", "United Kingdom"),
    ("IND", "India"),
    ("CHN", "China"),
    ("UG", "Uganda"),
]
CODITIONS_PRODUCTS_REUSE=[
    ("G", "Good"),
    ("B", "Bad"),
    ("E", "Excellent"),
    ("N", "New"),
    ("U", "Used"),
    ("R", "Refurbished"),
    ("D", "Damaged"),
    ("W", "Worn"),
    ("S", "Scratched"),
    ("C", "Cracked"),
    ("P", "Patched"),
    ("F", "Faded"),
]
ACTION = [
    ("T", "Transfer"),
    ("A", "Add"),
    
    ]
class ProfileUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=50)
    phone = models.CharField(_("Phone"), max_length=10)
    full_name = models.CharField(_("Full Name"), max_length=50, null=False, blank=False, default="")
    city = models.CharField(_("City"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="AD")
    country = models.CharField(_("Country"), max_length=50)
    country_origin = models.CharField(_("Country Origin"), max_length=50, choices=COUNTRIES, default="UAE")
    date_created = models.DateTimeField(_("Date Created"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, auto_now_add=False)
    email =     models.EmailField(_("email"), max_length=20, default="")
    user_type = models.CharField(_("User Type"), max_length=50, choices=CHOICES_FOR_USERS, default="CS")
    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_id = models.CharField(_("Unique Number"), max_length=30)
    product_name = models.CharField(_("Product Name"), max_length=50)
    manufacturer_name = models.CharField(_("Company Name"), max_length=50)
    manufacture_location = models.CharField(_("Location"), max_length=50,choices=MANUFACTURE_LOCATION_CHOICES, default="AD")
    product_type = models.CharField(_("Product Type"), max_length=50, choices=CHOICES_FOR_PRODUCTS, default="RC")
    product_quantity = models.PositiveIntegerField(_("Quantity"),default=1)
    product_mf_date = models.DateTimeField(_("Manufacturing Date"),default=datetime.datetime.now)
    product_expiry_date = models.DateTimeField(_("Expiry Date"), auto_now=False, auto_now_add=False,default=datetime.datetime.now)
    product_ownership = models.ForeignKey(ProfileUser, verbose_name=_("Owner"), on_delete=models.CASCADE, default=0)
    product_pdf = models.FileField(_("PDF QR Code"), upload_to="Added_Products/pdf_files", blank=True)
    product_qr_code = models.ImageField(_("QR Codes"), upload_to="Added_Products/Qr_codes")


    def __str__(self):
        return self.product_name


class Ownership(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="who_own_the_product", on_delete=models.CASCADE, default=0)
    status = models.CharField(_("Recycle Status"), max_length=10,choices=TRACK_STATUS, default="NO")
    new_owner = models.ForeignKey(ProfileUser, verbose_name=_("New Owner"), on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(_("Date"), auto_now=True)
    product_quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    action = models.CharField(_("Action"), max_length=50, default=" ")
    product_uid = models.CharField(_("Product Id"), max_length=30, default=None, null=True, blank=True)
    # Needs to be implemeted inorder to give the new user, a product qr code.
    # qr_code = models.FileField(_("QR Code"), upload_to="qr_codes/", blank=True)


    def __str__(self):
        return self.user.username 
      
class AddEvent(models.Model):
    event_name = models.CharField(_("Event Name"), max_length=50)
    event_date = models.DateTimeField(_("Event Date"), auto_now=False, auto_now_add=False)
    event_location = models.CharField(_("Location"), max_length=50)
    event_description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.event_name
    
    
class ReuseProducts(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE) 
    product_name = models.CharField(_("Product Name"), max_length=50)   
    product = models.CharField(_("Product"), max_length=50)
    product_quantity = models.IntegerField(_("Quantity"), default=1)
    product_catagories = models.CharField(_("Catagories"), max_length=3, choices=CHOICES_FOR_PRODUCTS, default="RU")
    product_description = models.TextField(_("Description"), blank=False, max_length=100)
    product_condition = models.CharField(_("Condition"), max_length=50,choices=CODITIONS_PRODUCTS_REUSE, default="Good")
    product_image = models.ImageField(_("Image"), upload_to="product_images/", blank=False, null=False)
    product_address = models.TextField(_("Address"), max_length=50)
    product_price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, default=0) 

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    product = models.ForeignKey(ReuseProducts, verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.product_price
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Full Name"), max_length=50)
    locality = models.CharField(_("Locality"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    zipcode = models.IntegerField(_("Zip Code"))
    state = models.CharField(_("State"), max_length=50)
    reg_date = models.DateField(_("Registration Date"))
    phone = models.IntegerField(_("Phone Number"))
    
    def __str__(self):
        return self.name