from django import forms
from django.forms import inlineformset_factory
from .models import Supplier, RecipeIngredient, Recipe, Product, Ingredient


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'email', 'phone', 'address']
        labels = {
            'name': 'Name',
            'ruc': 'RUC/Tax ID',
            'email': 'Email',
            'phone': 'Phone Number',
            'address': 'Address',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your tax ID'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'supplier', 'price_per_gram']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supply name'}),
            'price_per_gram': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per gram in [$/g]'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'shape', 'dimensions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe name'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dimensions of recipes '}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity_in_grams']

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_type', 'sale_price', 'recipe']
        labels = {
            'product_type': 'Product Type',
            'sale_price': 'Sale Price',
            'recipe': 'Recipe',
        }
        widgets = {
            'product_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product type'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter sale price'}),
            'recipe': forms.Select(attrs={'class': 'form-control'}),
        }
