from django.contrib import admin
from .models import Order, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'stripe_product_id')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student', 'product', 'created_at')
    list_filter = ('created_at',)
