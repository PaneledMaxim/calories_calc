from django import forms
from .models import FoodEntry


class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['product', 'grams', 'meal_type']