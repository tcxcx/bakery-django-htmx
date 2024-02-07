from django.urls import path
from .views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView
from .views import SupplyListView, SupplyCreateView, SupplyUpdateView, SupplyDeleteView
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from .views import PreparationListView, PreparationCreateView, PreparationUpdateView, PreparationDeleteView
from .views import ProductTableView, SupplierTableView, IngredientTableView, RecipeTableView
from .views import add_supplier, add_supply, add_recipe, add_product, add_product_type

app_name = "management"

urlpatterns = [
    # Supplier URLs
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/new/', SupplierCreateView.as_view(), name='new_supplier'),
    path('suppliers/<uuid:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/<uuid:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),

    # Supply URLs
    path('supplies/', SupplyListView.as_view(), name='supply-list'),
    path('supplies/new/', SupplyCreateView.as_view(), name='supply-create'),
    path('supplies/<int:pk>/update/', SupplyUpdateView.as_view(), name='supply-update'),
    path('supplies/<int:pk>/delete/', SupplyDeleteView.as_view(), name='supply-delete'),

    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/new/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Preparation URLs
    path('preparations/', PreparationListView.as_view(), name='preparation-list'),
    path('preparations/new/', PreparationCreateView.as_view(), name='preparation-create'),
    path('preparations/<int:pk>/update/', PreparationUpdateView.as_view(), name='preparation-update'),
    path('preparations/<int:pk>/delete/', PreparationDeleteView.as_view(), name='preparation-delete'),

    # Table URLs
    path('product-table/', ProductTableView.as_view(), name='product-table'),
    path('recipe-table/', RecipeTableView.as_view(), name='recipe-table'),
    path('supplier-table/', SupplierTableView.as_view(), name='supplier-table'),
    path('ingredient-table/', IngredientTableView.as_view(), name='ingredient-table'),

    # Form URLs
    path('supplier/add', add_supplier, name='add_supplier'),
    path('supply/add', add_supply, name='add_supply'),
    path('recipe/add', add_recipe, name='add_recipe'),
    path('product/add', add_product, name='add_product'),
    path('product-type/add', add_product_type, name='add_product_type'),
]
