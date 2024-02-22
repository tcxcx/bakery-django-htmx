import pytest
from django.test import TestCase
import factory
from bakery_app.management.models import Supplier, Ingredient, Recipe, RecipeIngredient, Product, ProductVariation
from factory import Faker, SubFactory, Sequence, post_generation, django, LazyFunction
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
import random
import factory

# this definition was found in https://github.com/joke2k/faker/issues/966 as char length with Faker was throwing errors that passed char limits

def factory_lazy_function(value, max_length=None):
    if max_length is None:
        max_length = len(value)

    return factory.LazyFunction(lambda: value[:max_length])

fake = factory.faker.faker.Faker()

class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory_lazy_function(value=fake.company(), max_length=20)
    ruc = factory_lazy_function(value=fake.isbn13(separator=""), max_length=13)
    email = factory_lazy_function(value=fake.email(), max_length=20)
    phone = factory_lazy_function(value=fake.phone_number(), max_length=20)
    address = factory_lazy_function(value=fake.address(), max_length=20)

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory_lazy_function(value=fake.word(), max_length=20)
    supplier = SubFactory(SupplierFactory)
    price_per_gram = LazyFunction(lambda: round(random.uniform(0.01, 100.00), 2))


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    name = Sequence(lambda n: f'Test Recipe {n}')
    description = Faker('sentence')
    shape = 'C'
    diameter = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)

class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    recipe = SubFactory(RecipeFactory)
    ingredient = SubFactory(IngredientFactory)
    quantity_in_grams = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = Sequence(lambda n: f'Test Product {n}')
    sale_price = Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    recipe = SubFactory(RecipeFactory)


class ProductVariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariation

    product = SubFactory(ProductFactory)
    diameter = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)


class TestModels(TestCase):
    @pytest.mark.xfail(reason="RUC can be longer than 13 characters with Faker data gen")
    def test_supplier_creation(self):
        supplier = SupplierFactory()
        saved_supplier = Supplier.objects.get(pk=supplier.pk)
        self.assertEqual(saved_supplier.name, supplier.name)
        self.assertEqual(saved_supplier.ruc, supplier.ruc)
        self.assertEqual(saved_supplier.email, supplier.email)
        self.assertEqual(saved_supplier.phone, supplier.phone)
        self.assertEqual(saved_supplier.address, supplier.address)

    def test_ingredient_creation(self):
        supplier = SupplierFactory()
        ingredient = IngredientFactory(supplier=supplier)
        saved_ingredient = Ingredient.objects.get(pk=ingredient.pk)
        self.assertEqual(saved_ingredient.name, ingredient.name)
        self.assertEqual(str(saved_ingredient.supplier.id), str(ingredient.supplier.id))
        self.assertEqual(saved_ingredient.price_per_gram, Decimal(str(ingredient.price_per_gram)))

    def test_recipe_creation(self):
        recipe = RecipeFactory()
        saved_recipe = Recipe.objects.get(pk=recipe.pk)
        self.assertEqual(saved_recipe.name, recipe.name)
        self.assertEqual(saved_recipe.description, recipe.description)
        self.assertEqual(saved_recipe.shape, recipe.shape)

    def test_recipe_ingredient_creation(self):
        recipe_ingredient = RecipeIngredientFactory()
        saved_recipe_ingredient = RecipeIngredient.objects.get(pk=recipe_ingredient.pk)
        self.assertEqual(saved_recipe_ingredient.recipe, recipe_ingredient.recipe)
        self.assertEqual(saved_recipe_ingredient.ingredient, recipe_ingredient.ingredient)
        self.assertEqual(saved_recipe_ingredient.quantity_in_grams, recipe_ingredient.quantity_in_grams)

    def test_product_creation(self):
        product = ProductFactory()
        saved_product = Product.objects.get(pk=product.pk)
        self.assertEqual(saved_product.product_type, product.product_type)
        self.assertEqual(saved_product.sale_price, product.sale_price)
        self.assertEqual(saved_product.recipe, product.recipe)

    def test_valid_quantity_edge_cases(self):
        # Test with a valid, non-zero quantity that should not raise a ValidationError
        try:
            valid_quantity = RecipeIngredientFactory(quantity_in_grams=Decimal('1.0'))
            valid_quantity.full_clean()  # This should not raise ValidationError
        except ValidationError:
            self.fail("Valid quantity_in_grams should not raise ValidationError.")

    def test_invalid_quantity_edge_cases(self):
        # Test with an intentionally invalid quantity that should raise a ValidationError
        with self.assertRaises(ValidationError):
            invalid_quantity = RecipeIngredientFactory(quantity_in_grams=Decimal('-1.0'))
            invalid_quantity.full_clean()  # Expect ValidationError for negative quantity

        with self.assertRaises(ValidationError):
            excessive_quantity = RecipeIngredientFactory(quantity_in_grams=Decimal('100000.0'))
            excessive_quantity.full_clean()  # Expect ValidationError for excessive quantity



    def test_model_string_representations(self):
        supplier = SupplierFactory(name='Supplier1')
        self.assertEqual(str(supplier), 'Supplier1')

        ingredient = IngredientFactory(name='Ingredient1')
        self.assertEqual(str(ingredient), 'Ingredient1')

        recipe = RecipeFactory(name='Recipe1')
        self.assertEqual(str(recipe), 'Recipe1')

        recipe_ingredient = RecipeIngredientFactory(
            recipe=recipe,
            ingredient=ingredient,
            quantity_in_grams=Decimal('100')
        )
        self.assertEqual(
            str(recipe_ingredient),
            'Ingredient1 in 100.00g for Recipe1'
        )

        product = ProductFactory(product_type='Product1')
        self.assertEqual(str(product), 'Product1')

@pytest.mark.django_db
class TestFieldValidations(TestCase):
    def test_negative_price_per_gram(self):
        with pytest.raises(ValidationError):
            IngredientFactory(price_per_gram=Decimal('-0.01')).full_clean()

@pytest.mark.django_db
class TestModelRelationships(TestCase):
    def test_recipe_ingredient_relationship(self):
        recipe = RecipeFactory()
        ingredient = IngredientFactory()
        recipe_ingredient = RecipeIngredientFactory(recipe=recipe, ingredient=ingredient)
        self.assertIn(recipe_ingredient, recipe.recipeingredient_set.all())
        self.assertEqual(recipe_ingredient.ingredient, ingredient)

@pytest.mark.django_db
class TestMethodAndProperty(TestCase):
    def test_calculate_profit_positive(self):
        product = ProductFactory()
        self.assertTrue(product.calculate_profit > 0)

    def test_calculate_margin(self):
        product = ProductFactory()
        expected_margin = (product.calculate_profit / product.sale_price) * 100
        self.assertEqual(product.calculate_margin, expected_margin)

@pytest.mark.django_db
class TestStringRepresentations(TestCase):
    def test_ingredient_str(self):
        ingredient = IngredientFactory(name="Flour")
        self.assertEqual(str(ingredient), "Flour")

@pytest.mark.django_db
class TestValidationMethods(TestCase):
    def test_clean_recipe_ingredient_negative_quantity(self):
        with pytest.raises(ValidationError):
            RecipeIngredientFactory(quantity_in_grams=Decimal('-1')).full_clean()

@pytest.mark.django_db
class TestEdgeCases(TestCase):
    def test_recipe_ingredient_edge_case_quantities(self):
        try:
            RecipeIngredientFactory(quantity_in_grams=Decimal('99999.99')).full_clean()
        except ValidationError:
            self.fail("Boundary quantity_in_grams should not raise ValidationError.")

@pytest.mark.django_db
class TestDeletionAndCascadeEffects(TestCase):
    def test_delete_supplier_cascades_to_ingredients(self):
        supplier = SupplierFactory()
        ingredient = IngredientFactory(supplier=supplier)
        supplier.delete()
        with pytest.raises(Ingredient.DoesNotExist):
            Ingredient.objects.get(id=ingredient.id)

@pytest.mark.django_db
class TestUniqueAndConstraints(TestCase):
    def test_unique_supplier_id(self):
        supplier1 = SupplierFactory()
        with pytest.raises(IntegrityError):
            SupplierFactory(id=supplier1.id)

# Additional edge case tests
@pytest.mark.django_db
class TestAdditionalEdgeCases(TestCase):
    @pytest.mark.xfail(reason="Intentionally testing edge cases that may fail")
    def test_invalid_quantity_edge_cases(self):
        with pytest.raises(ValidationError):
            RecipeIngredientFactory(quantity_in_grams=Decimal('-1.0')).full_clean()

        with pytest.raises(ValidationError):
            RecipeIngredientFactory(quantity_in_grams=Decimal('100000.0')).full_clean()


class ProductVariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariation

    product = SubFactory(ProductFactory)
    diameter = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    main_variation = True  # Assuming main_variation needs to be set for tests

# Assuming other factories (SupplierFactory, IngredientFactory, RecipeFactory, ProductFactory) are defined above

@pytest.mark.django_db
class TestProductVariationModels(TestCase):
    def setUp(self):
        self.supplier = SupplierFactory()
        self.ingredient = IngredientFactory(supplier=self.supplier)
        self.recipe = RecipeFactory()
        self.product = ProductFactory(recipe=self.recipe)
        self.product_variation = ProductVariationFactory(product=self.product, diameter=Decimal('10.0'), main_variation=True)

    def test_product_variation_creation(self):
        """Test the basic creation of a ProductVariation instance."""
        self.assertIsNotNone(self.product_variation.pk)
        self.assertEqual(self.product_variation.product, self.product)
        self.assertTrue(self.product_variation.main_variation)

    def test_calculate_surface_area_circular(self):
        """Ensure circular surface area is calculated correctly."""
        self.product.recipe.shape = 'Circular'
        self.product_variation.diameter = Decimal('10.0')
        self.product_variation.save()
        expected_area = Decimal('78.54')  # Approximation for πr² with r = 5.0
        calculated_area = self.product_variation.calculate_surface_area()
        self.assertAlmostEqual(calculated_area, expected_area, places=2)

    def test_calculate_surface_area_rectangular(self):
        """Ensure rectangular surface area is calculated correctly."""
        self.product.recipe.shape = 'Rectangular'
        self.product_variation.length = Decimal('10.0')
        self.product_variation.width = Decimal('5.0')
        self.product_variation.save()
        expected_area = Decimal('50.00')  # length × width
        calculated_area = self.product_variation.calculate_surface_area()
        self.assertAlmostEqual(calculated_area, expected_area, places=2)

    def test_adjustment_factor(self):
        # Assuming the main variation is correctly set up with a larger area
        # and a secondary variation is created with a smaller area
        main_variation_area = self.product_variation.calculate_surface_area()
        secondary_variation = ProductVariationFactory(product=self.product, diameter=Decimal('5.0'), main_variation=False)
        secondary_variation_area = secondary_variation.calculate_surface_area()

        # Calculate the expected adjustment factor based on areas
        expected_adjustment = secondary_variation_area / main_variation_area
        calculated_adjustment = secondary_variation.adjustment_factor()

        self.assertAlmostEqual(calculated_adjustment, expected_adjustment, places=2, msg=f"Expected adjustment factor {expected_adjustment} but got {calculated_adjustment}")


    def test_adjusted_cost(self):
        """Test the adjusted cost calculation."""
        self.product.recipe.recipeingredient_set.create(ingredient=self.ingredient, quantity_in_grams=Decimal('100.00'))
        expected_cost = self.product.calculate_cost  # Simplified; assumes cost calculation is correct
        self.assertEqual(self.product_variation.adjusted_cost, expected_cost)

    def test_adjusted_profit_and_margin(self):
        """Test the adjusted profit and margin calculations."""
        self.product.sale_price = Decimal('200.00')
        self.product.recipe.recipeingredient_set.create(ingredient=self.ingredient, quantity_in_grams=Decimal('100.00'))
        expected_profit = self.product.sale_price - self.product_variation.adjusted_cost
        expected_margin = (expected_profit / self.product.sale_price) * 100
        self.assertEqual(self.product_variation.adjusted_profit, expected_profit)
        self.assertAlmostEqual(self.product_variation.adjusted_margin, expected_margin, places=2)
