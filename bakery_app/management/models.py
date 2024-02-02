from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

import uuid


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Supply(models.Model):
    name = models.CharField(max_length=255)
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    SHAPE_CHOICES = [
        ('C', 'Circular'),
        ('R', 'Rectangular'),
    ]
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    shape = models.CharField(max_length=1, choices=SHAPE_CHOICES)
    dimensions = models.JSONField()

    def __str__(self):
        return self.name

    def calculate_cost(self):
        # Calculate the total cost of preparations for this product
        total_cost = self.preparation_set.aggregate(
            cost=ExpressionWrapper(
                Sum(F('supplies__price_per_gram') * F('supplies__quantity_in_grams')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )['cost']

        return total_cost

class Preparation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    supplies = models.ManyToManyField(Supply, through='PreparationSupply')

    def __str__(self):
        return self.name

    def calculate_cost(self):
    # Calculate the total cost of supplies for this preparation
        total_cost = self.supplies.aggregate(
            cost=Sum(models.F('supply__price_per_gram') * models.F('quantity_in_grams'))
        )['cost']
        return total_cost

class PreparationSupply(models.Model):
    preparation = models.ForeignKey(Preparation, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity_in_grams = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.supply.name} for {self.preparation.name}"
