from django.db import models
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, DecimalField
from decimal import Decimal

import uuid

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.name[:50]


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
    quantity_in_grams = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f"{self.ingredient.name} in {self.quantity_in_grams:.2f}g for {self.recipe.name}"

    def clean(self):

        if self.quantity_in_grams < 0:
            raise ValidationError({'quantity_in_grams': ["Quantity in grams cannot be negative.",]})

        if self.quantity_in_grams > 99999.99:
            raise ValidationError({'quantity_in_grams': ["Quantity in grams exceeds the maximum allowed value.",]})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(RecipeIngredient, self).save(*args, **kwargs)


class Product(models.Model):
    product_type = models.CharField(max_length=255)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.product_type

    @property
    def calculate_cost(self):
        total_cost = self.recipe.recipeingredient_set.aggregate(
            cost=Sum(F('quantity_in_grams') * F('ingredient__price_per_gram'), output_field=DecimalField())
        )['cost'] or Decimal('0.00')
        cost_rounded = round(total_cost, 2)
        return cost_rounded

    @property
    def calculate_profit(self):
        total_cost = self.calculate_cost
        cost_rounded = round(total_cost, 2)
        profit = self.sale_price - cost_rounded
        return round(profit, 2)



    @property
    def calculate_margin(self):
        margin_percentage = (self.calculate_profit / self.sale_price) * 100
        return round(margin_percentage, 2)

