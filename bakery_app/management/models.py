from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from django.utils.timezone import now
from math import pi
import uuid

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

class Supplier(AuditModel):
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    address = models.TextField()
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Ingredient(AuditModel):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.name[:50]

class Recipe(models.Model):
    SHAPE_CHOICES = [
        ('C', 'Circular'),
        ('R', 'Rectangular')
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    shape = models.CharField(max_length=1, choices=SHAPE_CHOICES)
    diameter = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')

    def __str__(self):
        return self.name

    def create_main_variation_for_product(self, product):
        """Automatically creates a main variation for the product based on this recipe."""
        ProductVariation.objects.create(
            product=product,
            diameter=self.diameter,
            length=self.length,
            width=self.width,
            main_variation=True
        )


class RecipeIngredient(AuditModel):
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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="products")

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.recipe.create_main_variation_for_product(self)
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    diameter = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    main_variation = models.BooleanField(default=False)

    def calculate_surface_area(self):
        if self.product.recipe.shape == 'Circular' and self.diameter:
            radius = self.diameter / 2
            surface_area = pi * (radius ** 2)
        elif self.product.recipe.shape == 'Rectangular' and self.length and self.width:
            surface_area = self.length * self.width
        else:
            surface_area = 0
        return surface_area


    def adjustment_factor(self):
        main_variation = self.product.variations.filter(main_variation=True).first()
        if main_variation:
            main_area = main_variation.calculate_surface_area()
            this_area = self.calculate_surface_area()
            if main_area > 0:
                return this_area / main_area
        return 1

    @property
    def adjusted_cost(self):
        adjustment_factor = self.adjustment_factor()
        return round(self.product.calculate_cost * adjustment_factor, 2)

    @property
    def adjusted_profit(self):
        return round(self.product.sale_price - self.adjusted_cost, 2)

    @property
    def adjusted_margin(self):
        if self.product.sale_price > 0:
            return round((self.adjusted_profit / self.product.sale_price) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.product.product_type} Variation ({'main' if self.main_variation else 'secondary'})"
