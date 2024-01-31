from django import forms
from .models import Supplier

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
