from django.contrib import admin
from .models import Product, OrderProduct, Order

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}

# admin.site.register(Product)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order)