from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'calories_per_100g']
        labels = {
            'name': 'Название',
            'calories_per_100g': 'Калории на 100г'
        }