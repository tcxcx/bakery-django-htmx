from django.contrib import admin
from .models import Supplier, Ingredient, Recipe, RecipeIngredient, Product, ProductVariation

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruc', 'email', 'phone', 'address')
    search_fields = ('name', 'ruc')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_gram', 'supplier')
    list_filter = ('supplier',)
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'shape')
    search_fields = ('name',)
    inlines = [RecipeIngredientInline,]

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity_in_grams')
    list_filter = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'sale_price', 'recipe')
    list_filter = ('product_type', 'recipe')
    search_fields = ('product_type',)

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'diameter', 'length', 'width', 'main_variation')
    list_filter = ('product', 'main_variation')
    search_fields = ('product__product_type',)
