import json

from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Supplier, Supply, Product, Preparation, Product
from .tables import ProductTable, RecipeTable, SupplierTable, IngredientTable
from django_tables2 import SingleTableView
from django.http import HttpResponse
from .forms import SupplierForm, SupplyForm, ProductTypeForm, ProductForm, PreparationForm, ProductCreationForm
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

class RecipeTableView(SingleTableView, View):
    model = Preparation
    table_class = RecipeTable
    template_name = 'management/suppliers/recipe_table.html'

class SupplierTableView(SingleTableView, View):
    model = Supplier
    table_class = SupplierTable
    template_name = 'management/suppliers/supplier_table.html'

class IngredientTableView(SingleTableView, View):
    model = Supply
    table_class = IngredientTable
    template_name = 'management/suppliers/ingredient_table.html'


# modals
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{supplier.name} added."
                    })
                })
    else:
        form = SupplierForm()
    return render(request, 'management/suppliers/form_supplier.html', {
        'form': form,
    })


def add_product_type(request):
    if request.method == "POST":
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            product = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{product.name} added."
                    })
                })
    else:
        form = ProductTypeForm()
    return render(request, 'management/suppliers/form_product.html', {
        'form': form,
    })

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{product.name} added."
                    })
                })
    else:
        form = ProductForm()
    return render(request, 'management/suppliers/form_product.html', {
        'form': form,
    })


def add_recipe(request):
    if request.method == "POST":
        form = PreparationForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{recipe.name} added."
                    })
                })
    else:
        form = PreparationForm()
    return render(request, 'management/suppliers/form_supplier.html', {
        'form': form,
    })

def add_supply(request):
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{supply.name} added."
                    })
                })
    else:
        form = SupplyForm()
    return render(request, 'management/suppliers/form_supply.html', {
        'form': form,
    })
