# management/tables.py
import django_tables2 as tables
from .models import Product

class ProductTable(tables.Table):
    total_cost = tables.Column(accessor='calculate_cost', verbose_name='Total Cost')
    margin_percentage = tables.Column(accessor='calculate_margin', verbose_name='Margin (%)')

    class Meta:
        model = Product
        fields = ['product_type', 'sale_price', 'total_cost', 'margin_percentage']
        template_name = 'django_tables2/bootstrap4.html'
