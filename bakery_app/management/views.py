from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Supplier, Supply, Product, Preparation, Product
from .tables import ProductTable
from django_tables2 import SingleTableView
from django.views import View

# Supplier views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'management/suppliers/form.html'
    context_object_name = 'suppliers'

class SupplierCreateView(CreateView):
    model = Supplier
    template_name = 'management/suppliers/form.html'
    fields = '__all__'

class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = 'management/suppliers/form.html'
    fields = '__all__'

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier-list')

# Supply views
class SupplyListView(ListView):
    model = Supply
    template_name = 'supply_list.html'
    context_object_name = 'supplies'

class SupplyCreateView(CreateView):
    model = Supply
    template_name = 'supply_form.html'
    fields = '__all__'

class SupplyUpdateView(UpdateView):
    model = Supply
    template_name = 'supply_form.html'
    fields = '__all__'

class SupplyDeleteView(DeleteView):
    model = Supply
    template_name = 'supply_confirm_delete.html'
    success_url = reverse_lazy('supply-list')

# Product views
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = '__all__'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = '__all__'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

# Preparation views
class PreparationListView(ListView):
    model = Preparation
    template_name = 'preparation_list.html'
    context_object_name = 'preparations'

class PreparationCreateView(CreateView):
    model = Preparation
    template_name = 'preparation_form.html'
    fields = '__all__'

class PreparationUpdateView(UpdateView):
    model = Preparation
    template_name = 'preparation_form.html'
    fields = '__all__'

class PreparationDeleteView(DeleteView):
    model = Preparation
    template_name = 'preparation_confirm_delete.html'
    success_url = reverse_lazy('preparation-list')



class ProductTableView(SingleTableView, View):
    model = Product
    table_class = ProductTable
    template_name = 'management/suppliers/product_table_htmx.html'
