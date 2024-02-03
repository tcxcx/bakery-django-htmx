import django_tables2 as tables
from .models import Product

class ProductTable(tables.Table):
    total_cost = tables.Column(accessor='calculate_cost')
    margin = tables.Column(accessor='calculate_margin')

    class Meta:
        model = Product
        fields = ['name', 'shape', 'dimensions', 'total_cost', 'sale_price', 'margin']
        template_name = "tables/bootstrap_htmx.html"
