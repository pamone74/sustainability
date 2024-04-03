from django.contrib import admin
from .models import Manufacturer, Product, Users, Ownership

# Register your models here.
# class ProductInline(admin.TabularInline):
    # model = Product
# class ManufacturerAdmin(admin.ModelAdmin):'manufacture_location', 'product_type', 'product_quantity', 'product_mf_date', 'product_expiry_date')
    # inlines = [ProductInline,]
# class ProdcutAdmin(admin.ModelAdmin):
    # # list_display = ('product_name', 'manufacturer_name', 'product_type', 'product_quantity', 'product_ownership')
# admin.site.register(Manufacturer, ManufacturerAdmin)
# admin.site.register(Product, ProdcutAdmin)

admin.site.register(Manufacturer)
#admin.site.register(Product)
# admin.site.register(Ownership)
@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('user','get_property','product_quantity', 'status')
    def get_property(self, obj):
        product_names = [product.product_name for product in obj.product.all()]
        return ', '.join(product_names) if product_names else None
    def get_quantity(self, obj):
        return obj.user.product_quantity if obj.user.product_quantity else obj.user.product_quantity
    ordering = ('user',)
    search_fields = ('user',)
    filter = ('product',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer_name', 'product_type', 'product_quantity', 'product_ownership')
    search_fields = ('product_name', 'manufacturer_name')
    list_filter = ('product_type', 'product_ownership')
    ordering = ('product_name', 'manufacturer_name')
