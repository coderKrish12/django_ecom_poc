
from django.contrib import admin
from .models import Category, Product, ProductImage, Inventory, Stock, Attribute, AttributeValue, Cart, CartItem

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description','slug'] 

class InventoryAdmin(admin.ModelAdmin): 
    search_fields = ['product__name', 'product__description','product__slug']

class StockAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'product__description','product__slug']

class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'product__description','product__slug']

class AttributeAdmin(admin.ModelAdmin):
    search_fields = ['name']

class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ['attribute__name', 'value']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['cart__user__first_name', 'cart__user__last_name', 'cart__user__email']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)