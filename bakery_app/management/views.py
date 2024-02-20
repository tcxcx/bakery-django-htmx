import json

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Supplier, Ingredient, Recipe, Product
from .tables import ProductTable
from django_tables2 import SingleTableView
from django.http import HttpResponse
from .forms import RecipeForm, RecipeIngredientForm, Recipe, RecipeIngredient, SupplierForm, ProductForm, IngredientForm
from django.views import View
from django.forms import inlineformset_factory

# Supplier views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'management/suppliers/list.html'
    context_object_name = 'suppliers'

class SupplierCreateView(CreateView):
    model = Supplier
    template_name = 'management/suppliers/create_update.html'
    fields = '__all__'
    success_url = reverse_lazy('management:supplier-list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    success_url = reverse_lazy('management:supplier-list')
    fields = '__all__'

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'list.html'
    success_url = reverse_lazy('management:supplier-list')

# Ingredient views (replacing Supply views)
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'management/suppliers/list.html'
    context_object_name = 'ingredients'

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'management/suppliers/create_update.html'
    success_url = reverse_lazy('management:ingredient-list')

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'management/suppliers/create_update.html'
    success_url = reverse_lazy('management:ingredient-list')

class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'management/suppliers/create_update.html'
    success_url = reverse_lazy('management:ingredient-list')


# Product views
class ProductListView(ListView):
    model = Product
    template_name = 'management/suppliers/form_product.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'management/suppliers/form_product.html'
    fields = '__all__'
    success_url = reverse_lazy('management:product-list')

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'management/suppliers/form_product.html'
    fields = '__all__'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'form_product.html'
    success_url = reverse_lazy('management:product-list')

# Recipe views
class RecipeListView(ListView):
    model = Recipe
    template_name = 'management/suppliers/list.html'
    context_object_name = 'recipes'

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    fields=['ingredient', 'quantity_in_grams'],
    extra=3,
    can_delete=True
)

class RecipeCreateView(View):
    template_name = 'management/suppliers/create_update.html'

    def get(self, request, *args, **kwargs):
        form = RecipeForm()
        formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect('management:product-list')
        return render(request, self.template_name, {'form': form, 'formset': formset})


class RecipeUpdateView(View):
    template_name = 'management/suppliers/create_update.html'

    def get(self, request, pk, *args, **kwargs):
        recipe = Recipe.objects.get(pk=pk)
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'recipe': recipe})

    def post(self, request, pk, *args, **kwargs):
        recipe = Recipe.objects.get(pk=pk)
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('management:recipe-list')
        return render(request, self.template_name, {'form': form, 'formset': formset, 'recipe': recipe})

# table view

class ProductTableView(SingleTableView, View):
    model = Product
    table_class = ProductTable
    template_name = 'management/suppliers/product_table_htmx.html'

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
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"{recipe.name} added successfully."
                    })
                })
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
    return render(request, 'management/suppliers/form_recipe.html', {
        'form': form,
        'formset': formset,
    })


def add_ingredient(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
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
        form = IngredientForm()
    return render(request, 'management/suppliers/form_ingredient.html', {
        'form': form,
    })
