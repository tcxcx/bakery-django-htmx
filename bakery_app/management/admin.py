from django.contrib import admin
from .models import Supplier, Supply, ProductType, Product, Preparation

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruc', 'email', 'phone', 'address')
    search_fields = ('name', 'ruc')

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_gram', 'supplier')
    list_filter = ('supplier',)
    search_fields = ('name',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'sale_price', 'shape')
    list_filter = ('product_type', 'shape')
    search_fields = ('name',)

@admin.register(Preparation)
class PreparationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')
    list_filter = ('product',)
    search_fields = ('name',)
