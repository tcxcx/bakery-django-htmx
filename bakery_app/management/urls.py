from django.urls import path
from .views import list_suppliers, supplier_form, delete_supplier

urlpatterns = [
    path('suppliers/', list_suppliers, name='list_suppliers'),
    path('suppliers/new/', supplier_form, name='new_supplier'),
    path('suppliers/<int:pk>/edit/', supplier_form, name='edit_supplier'),
    path('suppliers/<int:pk>/delete/', delete_supplier, name='delete_supplier'),
]
