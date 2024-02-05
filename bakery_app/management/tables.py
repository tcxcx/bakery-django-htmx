# management/tables.py
import django_tables2 as tables
from .models import Product

class ProductTable(tables.Table):
    class Meta:
        model = Product
        fields = ['name', 'shape', 'dimensions', 'sale_price', 'calculate_cost', 'calculate_margin']
        template_name = 'django_tables2/bootstrap4.html'  # Use Bootstrap styling

    # Add custom columns or modify existing ones as needed
    calculate_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost')
    calculate_margin = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')
