from django.urls import path
from .views import (
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView,
    IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    RecipeListView, RecipeCreateView, RecipeUpdateView,
    ProductTableView, VariationsTableView,
    add_supplier, add_recipe, add_product, add_ingredient, product_list_view, add_product_variation
)
from . import views


app_name = "management"

urlpatterns = [
    # Supplier URLs
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/new/', SupplierCreateView.as_view(), name='supplier-create'),
    path('suppliers/<uuid:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/<uuid:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),

    # Ingredient URLs
    path('ingredients/', IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/new/', IngredientCreateView.as_view(), name='ingredient-create'),
    path('ingredients/<int:pk>/update/', IngredientUpdateView.as_view(), name='ingredient-update'),
    path('ingredients/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient-delete'),

    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/new/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Recipe URLs
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),

    # Modal and Table URLs
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_product/', add_product, name='add_product'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('add_ingredient/', add_ingredient, name='add_ingredient'),
    path('add_product_variation/', add_product_variation, name='add_product_variation'),


    path('product-table/', ProductTableView.as_view(), name='product-table'),
    path('products/', product_list_view, name='product-list'),
    path('update_variation_form/<int:product_id>/', views.update_variation_form, name='update_variation_form'),
    path('get_product_shape/<int:product_id>/', views.get_product_shape, name='get_product_shape'),
    path('variations-table/', VariationsTableView.as_view(), name='variations-table'),

]
