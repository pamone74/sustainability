from django.db import models

# Create your models here.
class Products(models.Models):
    RECYCABLE = "RC"
    NON_RECYCABLE = "NRC"

    product_choices =
    {
        "RC": "recyble",
        "NRC": "non recycable"
    }
    product_id = models.IntegerField()
    product_qr = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    product_expiry = models.IntegerField()
    select = models.CharField(max_length=3, choice=product_choices,default="RC")

class User(models.Model):
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    user_email = models.CharField(max_length=50)
    user_tel = models.IntegerField(null=false)
    user_name = models.CharField(max_length=10)
    user_first_name = models.CharField( max_length=50)
    user_last_name =models.CharField(max_length=50)