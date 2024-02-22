import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Supplier, Ingredient, Recipe, Product, ProductVariation
from django.http import HttpResponse
from .tables import ProductTable, ProductVariationTable, IngredientTable
from django.http import JsonResponse
from django_tables2 import SingleTableView
from django.http import HttpResponseRedirect
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .filters import ProductFilter
from django.http import HttpResponse
from .forms import RecipeForm, RecipeIngredientForm, Recipe, RecipeIngredient, SupplierForm, ProductForm, IngredientForm, ProductVariationForm
from django.views import View
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from .forms import ProductVariationFormSet
from django.template.loader import render_to_string

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
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.POST:
                context['variations_formset'] = ProductVariationFormSet(self.request.POST)
            else:
                context['variations_formset'] = ProductVariationFormSet()
            return context

    def form_valid(self, form):
        context = self.get_context_data()
        variations_formset = context['variations_formset']
        if variations_formset.is_valid():
            self.object = form.save()
            variations_formset.instance = self.object
            variations_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'management/suppliers/form_product.html'
    success_url = reverse_lazy('management:product-list')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['variations_formset'] = ProductVariationFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['variations_formset'] = ProductVariationFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variations_formset = context['variations_formset']
        if variations_formset.is_valid():
            response = super(ProductUpdateView, self).form_valid(form)
            variations_formset.instance = self.object
            variations_formset.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        variations = product.variations.all()
        for variation in variations:
            variation.adjusted_supplies = variation.get_adjusted_supplies()
            variation.adjusted_cost = variation.calculate_adjusted_cost()
            variation.profit = variation.calculate_profit()
            variation.margin = variation.calculate_margin()
        context['variations'] = variations
        return context


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

class ProductTableView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'management/suppliers/product_table_htmx.html'
    filterset_class = ProductFilter
    paginate_by = 10

class IngredientTableView(SingleTableMixin, FilterView):
    model = Ingredient
    table_class = IngredientTable
    template_name = 'management/suppliers/ingredient_table_htmx.html'
    filterset_class = ProductFilter
    paginate_by = 10

class VariationsTableView(SingleTableMixin, FilterView):
    model = ProductVariation
    table_class = ProductVariationTable
    template_name = 'management/suppliers/variations_table.html'


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
                        "showMessage": f"{product.product_type} added."
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

def add_product_variation(request):
    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        if form.is_valid():
            product_variation = form.save()
            return HttpResponse(
                            status=204,
                            headers={
                                'HX-Trigger': json.dumps({
                                    "showMessage": f"Product variation added."
                                })
                            })
    else:
        form = ProductVariationForm()
    return render(request, 'management/suppliers/form_add_product_variation.html', {'form': form})


def product_list_view(request):
    filter = ProductFilter(request.GET, queryset=Product.objects.all())
    table = ProductTable(filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    if request.htmx:
        return render(request, 'management/suppliers/product_table_partial.html', {'table': table})
    else:
        return render(request, 'management/suppliers/product_table_htmx.html', {'table': table, 'filter': filter})

def update_variation_form(request, product_id):
    product = Product.objects.get(pk=product_id)
    return JsonResponse({
        'shape': product.recipe.shape
    })

def get_product_shape(request, product_id):
    product = Product.objects.get(pk=product_id)
    shape = product.recipe.shape
    return JsonResponse({'shape': shape})
