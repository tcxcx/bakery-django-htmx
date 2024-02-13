from django import forms
from django.forms import inlineformset_factory, ModelChoiceField
from .models import Supplier, Ingredient, Recipe, RecipeIngredient, Product

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'supplier', 'price_per_gram']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_gram': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'shape', 'dimensions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'shape': forms.Select(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RecipeIngredientForm(forms.ModelForm):
    ingredient = ModelChoiceField(queryset=Ingredient.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity_in_grams = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity_in_grams']

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    fields=['ingredient', 'quantity_in_grams'],
    extra=1,
    can_delete=True
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_type', 'sale_price', 'recipe']
        widgets = {
            'product_type': forms.TextInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'recipe': forms.Select(attrs={'class': 'form-control'}),
        }
