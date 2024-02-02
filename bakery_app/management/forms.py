from django import forms
from .models import Supplier, PreparationSupply, Preparation, Product, ProductType, Supply

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

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'price_per_gram', 'supplier']
        labels = {
            'name': 'Name',
            'price_per_gram': 'Price per Gram',
            'supplier': 'Supplier',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supply name'}),
            'price_per_gram': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per gram'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['name']
        labels = {
            'name': 'Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product type name'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'sale_price', 'shape', 'dimensions']
        labels = {
            'name': 'Name',
            'product_type': 'Product Type',
            'sale_price': 'Sale Price',
            'shape': 'Shape',
            'dimensions': 'Dimensions (JSON)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter sale price'}),
            'shape': forms.Select(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dimensions in JSON format'}),
        }

class PreparationForm(forms.ModelForm):
    class Meta:
        model = Preparation
        fields = ['product', 'name', 'supplies']
        labels = {
            'product': 'Product',
            'name': 'Name',
            'supplies': 'Supplies',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter preparation name'}),
            'supplies': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class PreparationSupplyForm(forms.ModelForm):
    class Meta:
        model = PreparationSupply
        fields = ['preparation', 'supply', 'quantity_in_grams']
        labels = {
            'preparation': 'Preparation',
            'supply': 'Supply',
            'quantity_in_grams': 'Quantity in Grams',
        }
        widgets = {
            'preparation': forms.Select(attrs={'class': 'form-control'}),
            'supply': forms.Select(attrs={'class': 'form-control'}),
            'quantity_in_grams': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity in grams'}),
        }
