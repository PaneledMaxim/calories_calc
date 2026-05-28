from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'calories_per_100g', 'protein_per_100g', 'fat_per_100g', 'carbs_per_100g']
        labels = {
            'name': 'Название',
            'calories_per_100g': 'Калории на 100г',
            'protein_per_100g': 'Белки на 100г',
            'fat_per_100g': 'Жиры на 100г',
            'carbs_per_100g': 'Углеводы на 100г'
        }