from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    search_fields = ['name']
    list_filter = ['category']
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
