from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
CATAGORY_CHOICES=[
    ("RC", "Recycable"),
    ("NR", "Non Recycable"),
    ("RCV", "Recover"),
    ("RU", "Reuse"),
]
class Product(models.Model):
    title = models.CharField(_("Product title"), max_length=50)
    selling_price = models.FloatField(_("Price"))
    discounted_price = models.FloatField(_("Discount"))
    description = models.TextField(_("Description"), default="")
    prodapp = models.TextField(_("I don't know"), default="")
    catagory = models.CharField(_("Catagories"), max_length=3, choices=CATAGORY_CHOICES)
    product_img = models.ImageField(_("Images"), upload_to='product')

    def __str__(self):
        return self.title