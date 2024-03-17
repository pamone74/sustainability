from django.contrib import admin
from .models import Manufacturer, Product

# Register your models here.
class ProductInline(admin.TabularInline):
    model = Product
class ManufacturerAdmin(admin.ModelAdmin):
    # fieldsets = [
        # (None,               {'fields': ['product_name']}),
        # ('Date information', {'fields': ['product_mf_date'], 'classes': ['collapse']}),
    # ]
    inlines = [ProductInline,]
class ProdcutAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer_name', 'product_type', 'product_quantity', 'product_ownership')
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Product, ProdcutAdmin)