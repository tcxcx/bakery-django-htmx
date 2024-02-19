import pytest
from django.test import TestCase
import factory
from bakery_app.management.models import Supplier, Ingredient, Recipe, RecipeIngredient, Product
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
    dimensions = {'diameter': 10}

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
        self.assertEqual(saved_recipe.dimensions, recipe.dimensions)

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
