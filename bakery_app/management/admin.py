from django.contrib import admin
from .models import Supplier, Supply, ProductType, Product, Preparation

admin.site.register(Supplier)
admin.site.register(Supply)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Preparation)
