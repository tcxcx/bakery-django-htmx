# management/tables.py
import django_tables2 as tables
from .models import Product, ProductVariation

class ProductTable(tables.Table):
    total_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost $USD')
    profit = tables.Column(accessor='calculate_profit', verbose_name='Profit $USD')
    margin_percentage = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')

    class Meta:
        model = Product
        fields = ['product_type', 'sale_price', 'total_cost', 'profit', 'margin_percentage']
        template_name = 'django_tables2/bootstrap4.html'


class ProductVariationTable(tables.Table):
    product_type = tables.Column(accessor='product.product_type')
    shape = tables.Column(accessor='product.recipe.shape')
    dimensions = tables.TemplateColumn(template_name='management/suppliers/variations_dimensions_column.html')

    class Meta:
        model = ProductVariation
        fields = ['product_type', 'shape', 'dimensions']
        template_name = 'django_tables2/bootstrap4.html'

