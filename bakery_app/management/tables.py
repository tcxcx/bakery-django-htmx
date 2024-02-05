# management/tables.py
import django_tables2 as tables
from .models import Product, Preparation, Supply, Supplier

class ProductTable(tables.Table):
    class Meta:
        model = Product
        fields = ['name', 'shape', 'dimensions', 'sale_price', 'calculate_cost', 'calculate_margin']
        template_name = 'django_tables2/bootstrap4.html'

    calculate_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost')
    calculate_margin = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')

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
