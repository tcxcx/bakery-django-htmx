from decimal import Decimal
from django.db.models import Q
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    class Meta:
        model = Product
        fields = ['query']

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return Product.objects.filter(
                Q(sale_price=value) | Q(total_cost=value)
            )

        return Product.objects.filter(
            Q(name__icontains=value) | Q(shape__icontains=value)
        )
