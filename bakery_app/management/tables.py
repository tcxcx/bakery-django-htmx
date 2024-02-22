# management/tables.py
import django_tables2 as tables
from .models import Product, ProductVariation, Ingredient

class ProductTable(tables.Table):
    total_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost $USD')
    profit = tables.Column(accessor='calculate_profit', verbose_name='Profit $USD')
    margin_percentage = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')

    class Meta:
        model = Product
        fields = ['product_type', 'sale_price', 'total_cost', 'profit', 'margin_percentage']
        template_name = 'django_tables2/bootstrap4.html'


class IngredientTable(tables.Table):
    name = tables.Column(verbose_name='Ingredient Name')
    weight = tables.Column(accessor='price_per_gram', verbose_name='Weight (grams)')

    class Meta:
        model = Ingredient
        fields = ('name', 'weight')
        template_name = 'django_tables2/bootstrap4.html'


class ProductVariationTable(tables.Table):
    product_type = tables.Column(accessor='product.product_type')
    shape = tables.Column(accessor='product.recipe.shape')
    dimensions = tables.TemplateColumn(template_name='management/suppliers/variations_dimensions_column.html')
    adjusted_cost = tables.Column(accessor='adjusted_cost', verbose_name='Adjusted Cost $USD')
    adjusted_profit = tables.Column(accessor='adjusted_profit', verbose_name='Profit $USD')
    adjusted_margin = tables.Column(accessor='adjusted_margin', verbose_name='Margin (%)')

    class Meta:
        model = ProductVariation
        fields = ['product_type', 'shape', 'dimensions', 'adjusted_cost', 'adjusted_profit', 'adjusted_margin']
        template_name = 'django_tables2/bootstrap4.html'
