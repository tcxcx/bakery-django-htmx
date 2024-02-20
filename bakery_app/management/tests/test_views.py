import pytest
from django.urls import reverse
from http import HTTPStatus
from bakery_app.management.models import Supplier, Ingredient, Recipe, Product
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(email='testuser@example.com', password='12345')

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(name='Test Supplier', ruc='123456789', email='supplier@example.com', phone='1234567890', address='123 Test St')

@pytest.fixture
def ingredient(db):
    return Ingredient.objects.create(name='Flour', price_per_gram='2.50')

@pytest.fixture
def recipe(db, ingredient):
    recipe = Recipe.objects.create(name='Bread', description='Basic bread recipe.')
    recipe.ingredients.add(ingredient)
    return recipe

@pytest.fixture
def product(db):
    return Product.objects.create(name='Bakery Product', price_per_gram='5.00')

# Supplier Tests
@pytest.mark.django_db
def test_supplier_list_view(client, user):
    client.force_login(user)
    url = reverse('management:supplier-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
def test_supplier_create_view(client, user):
    client.force_login(user)
    url = reverse('management:supplier-create')
    data = {'name': 'New Supplier', 'ruc': '987654321', 'email': 'new@example.com', 'phone': '9876543210', 'address': '456 New St'}
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.FOUND
    assert Supplier.objects.filter(name='New Supplier').exists()


@pytest.mark.django_db
def test_supplier_update_view(client, user, supplier):
    client.force_login(user)
    url = reverse('management:supplier-update', kwargs={'pk': supplier.pk})
    data = {'name': 'Updated Supplier', 'ruc': '987654321', 'email': 'update@example.com', 'phone': '9876543210', 'address': 'Updated Address'}
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.FOUND, "Update should redirect"
    supplier.refresh_from_db()
    assert supplier.name == 'Updated Supplier', "Supplier name should be updated"

@pytest.mark.django_db
def test_supplier_delete_view(client, user, supplier):
    client.force_login(user)
    url = reverse('management:supplier-delete', kwargs={'pk': supplier.pk})
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND, "Delete should redirect"
    assert not Supplier.objects.filter(pk=supplier.pk).exists(), "Supplier should be deleted"


# Ingredient Tests
# Follow the pattern established above for Supplier tests, replacing the model, form data, and URLs as appropriate.

# Recipe Tests
@pytest.mark.django_db
def test_recipe_list_view(client, user):
    client.force_login(user)
    url = reverse('management:recipe-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

# @pytest.mark.django_db
# def test_recipe_create_view(client, user, ingredient):
#     client.force_login(user)
#     url = reverse('management:recipe-create')
#     data = {
#         'name': 'Test Recipe',
#         'description': 'A test recipe',
#         'recipeingredient_set-TOTAL_FORMS': '1',
#         'recipeingredient_set-INITIAL_FORMS': '0',
#         'recipeingredient_set-MIN_NUM_FORMS': '0',
#         'recipeingredient_set-0-ingredient': ingredient.pk,
#         'recipeingredient_set-0-quantity_in_grams': '100',
#     }
#     response = client.post(url, data)
#     assert response.status_code == HTTPStatus.FOUND

#     assert Recipe.objects.filter(name='Test Recipe').exists()

# Product Tests
@pytest.mark.django_db
def test_product_list_view(client, user):
    client.force_login(user)
    url = reverse('management:product-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Ingredient Update Test
@pytest.mark.django_db
def test_ingredient_update_view(client, user, ingredient):
    client.force_login(user)
    url = reverse('management:ingredient-update', args=[ingredient.pk])
    data = {'name': 'Flour', 'cost': '3.00'}
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.OK
    ingredient.refresh_from_db()
    assert ingredient.name == 'Flour'

# Ingredient Delete Test
@pytest.mark.django_db
def test_ingredient_delete_view(client, user, ingredient):
    client.force_login(user)
    url = reverse('management:ingredient-delete', args=[ingredient.pk])
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Ingredient.objects.filter(pk=ingredient.pk).exists()


@pytest.mark.django_db
def test_add_supplier(client, user):
    client.force_login(user)
    url = reverse('management:add_supplier')
    data = {
        'name': 'Test Supplier',
        'ruc': '123456789',
        'email': 'supplier@example.com',
        'phone': '1234567890',
        'address': '123 Test St'
    }
    response = client.post(url, data)
    assert response.status_code == 204
    assert Supplier.objects.filter(name='Test Supplier').exists()
    assert 'HX-Trigger' in response.headers


# @pytest.mark.django_db
# def test_add_product(client, user):
#     client.force_login(user)
#     # Prepare the dimensions and shape for the Recipe instance
#     dimensions_data = {"length": 24, "width": 15, "height": 5}
#     shape = 'C'  # Example shape value

#     # Create a Recipe instance with the necessary dimensions and shape
#     recipe_instance = Recipe.objects.create(
#         name='Sample Recipe',
#         description='Sample Description',
#         shape=shape,
#         dimensions=json.dumps(dimensions_data)
#     )

#     url = reverse('management:add_product')
#     data = {
#         'product_type': 'Test Product Type',
#         'sale_price': '10.00',
#         'recipe': recipe_instance.id,  # Associate with the created Recipe instance
#     }

#     response = client.post(url, data)
#     # Ensure the response status code is either 200 or 204
#     assert response.status_code in [200, 204], "Expected HTTP 200/204 response"
#     # Verify that the Product instance has been created successfully
#     assert Product.objects.filter(product_type='Test Product Type').exists(), "Product should be created"


# @pytest.mark.django_db
# def test_add_recipe(client, user, ingredient):
#     client.force_login(user)
#     url = reverse('management:add_recipe')
#     data = {
#         'name': 'Test Recipe',
#         'description': 'A test recipe description',
#         # Assume 'ingredient' fixture is an Ingredient instance
#         'recipeingredient_set-INITIAL_FORMS': '0',
#         'recipeingredient_set-TOTAL_FORMS': '1',
#         'recipeingredient_set-0-ingredient': ingredient.pk,
#         'recipeingredient_set-0-quantity_in_grams': '100'
#     }
#     response = client.post(url, data)
#     assert response.status_code ==  200
#     assert Recipe.objects.filter(name='Test Recipe').exists()
#     assert 'HX-Trigger' in response.headers


# @pytest.mark.django_db
# def test_add_ingredient(client, user):
#     client.force_login(user)
#     url = reverse('management:add_ingredient')
#     data = {
#         'name': 'Test Ingredient',
#         'price_per_gram': '2.50'
#     }
#     response = client.post(url, data)
#     assert response.status_code ==  200
#     assert Ingredient.objects.filter(name='Test Ingredient').exists()
#     assert 'HX-Trigger' in response.headers
