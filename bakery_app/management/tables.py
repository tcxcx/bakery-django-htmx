# management/tables.py
import django_tables2 as tables
from .models import Product, Preparation, Supply, Supplier


class ProductTable(tables.Table):
    total_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost')
    margin_percentage = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')

    class Meta:
        model = Product
        fields = ['name', 'shape', 'dimensions', 'sale_price', 'total_cost', 'margin_percentage']
        template_name = 'django_tables2/bootstrap4.html'

class RecipeTable(tables.Table):
    class Meta:
        model = Preparation
        fields = ['name', 'product', 'supplies']
        template_name = 'django_tables2/bootstrap4.html'

class SupplierTable(tables.Table):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'email', 'phone', 'address', 'created']
        template_name = 'django_tables2/bootstrap4.html'

class IngredientTable(tables.Table):
    class Meta:
        model = Supply
        fields = ['name', 'price_per_gram', 'supplier']
        template_name = 'django_tables2/bootstrap4.html'
