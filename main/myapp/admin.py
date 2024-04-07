from django.contrib import admin
from .models import Product, Ownership, AddEvent,ReuseProducts

@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('user','get_property','product_quantity', 'status', 'new_owner', 'action','product_uid','date')
    def get_property(self, obj):
        if hasattr(obj, 'product'):
            if hasattr(obj.product, 'all') and callable(obj.product.all):
                # obj.product is a queryset
                product_names = [product.product_name for product in obj.product.all()]
            else:
                product_names = [obj.product.product_name]
            return ', '.join(product_names) if product_names else None
        return None
    # def get_quantity(self, obj):
        # return obj.user.product_quantity if obj.user.product_quantity else obj.user.product_quantity
    ordering = ('user',)
    search_fields = ('user',)
    filter = ('product',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_name', 'manufacturer_name', 'product_type', 'product_quantity', 'product_ownership',"product_pdf","product_qr_code")
    search_fields = ('product_name', 'manufacturer_name')
    list_filter = ('product_type', 'product_ownership')
    ordering = ('product_name', 'manufacturer_name')
@admin.register(ReuseProducts)
class ReuseProductsAdmin(admin.ModelAdmin):
    list_display = ('user','product_name', 'product_catagories', 'product_condition', 'product_quantity', 'product_image')
    search_fields = ('product_name', 'product_catagories')
    list_filter = ('product_catagories', 'product_name')
    ordering = ('product_catagories', 'product_name')