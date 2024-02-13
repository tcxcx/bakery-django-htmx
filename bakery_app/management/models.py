from django.db import models
from django.db.models import Sum, F, DecimalField
from decimal import Decimal

import uuid

# the supplier of a given ingredient
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

# this should be similar to Tag model
class Ingredient (models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# this should be similar to Post model
class Recipe (models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    shape_options = [
    ('C', 'Circular'),
    ('R', 'Rectangular'),
    ]
    shape = models.CharField(max_length=1, choices=shape_options)
    dimensions = models.JSONField()

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)
    quantity_in_grams = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ingredient.name} in {self.quantity_in_grams}g for {self.recipe.name}"


class Product(models.Model):
    product_type = models.CharField(max_length=255)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    @property
    def calculate_cost(self):
        total_cost = self.recipe.recipeingredient_set.aggregate(
            cost=Sum(F('quantity_in_grams') * F('ingredient__price_per_gram'), output_field=DecimalField())
        )['cost'] or Decimal('0.00')
        cost_rounded = round(total_cost, 2)
        return cost_rounded

    @property
    def calculate_margin(self):
        total_cost = self.calculate_cost
        cost_rounded = round(total_cost, 2)
        margin = self.sale_price - cost_rounded
        return margin
