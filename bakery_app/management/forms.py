from django import forms
from django.forms import inlineformset_factory, ModelChoiceField
from .models import Supplier, Ingredient, Recipe, RecipeIngredient, Product, ProductVariation

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
        fields = ['name', 'description', 'shape', 'diameter', 'length', 'width']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'shape': forms.Select(attrs={'class': 'form-control'}),
            'diameter': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        # Initial visibility of the dimension fields based on 'shape' selection
        self.fields['diameter'].required = False
        self.fields['length'].required = False
        self.fields['width'].required = False

        # Dynamically adjust required fields based on 'shape' field
        if self.data.get('shape') == 'C':
            self.fields['diameter'].required = True
        elif self.data.get('shape') == 'R':
            self.fields['length'].required = True
            self.fields['width'].required = True

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

    def save(self, commit=True):
        # Save the Product instance
        product_instance = super(ProductForm, self).save(commit=False)
        if commit:
            product_instance.save()
            # Assuming the Recipe instance is already linked to the Product
            recipe_instance = product_instance.recipe
            # Check if dimensions are provided in the Recipe and create main ProductVariation
            if recipe_instance and (recipe_instance.diameter or (recipe_instance.length and recipe_instance.width)):
                ProductVariation.objects.create(
                    product=product_instance,
                    diameter=recipe_instance.diameter,
                    length=recipe_instance.length,
                    width=recipe_instance.width,
                    main_variation=True
                )
        return product_instance


class ProductVariationForm(forms.ModelForm):

    class Meta:
        model = ProductVariation
        fields = ['product', 'diameter', 'length', 'width']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateFormFields();'}),
            'diameter': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        instance = super(ProductVariationForm, self).save(commit=False)
        if instance.main_variation:
            ProductVariation.objects.filter(product=instance.product).update(main_variation=False)
        if commit:
            instance.save()
        return instance

ProductVariationFormSet = inlineformset_factory(Product, ProductVariation, form=ProductVariationForm, extra=1, can_delete=True)
