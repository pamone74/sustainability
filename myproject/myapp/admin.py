from django.contrib import admin
from .models import Manufacturer, Products

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Products)