from django.db import models
from products.models import Product
from django.conf import settings

class FoodEntry(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    grams = models.PositiveIntegerField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} — {self.grams}г"

    @property
    def calories(self):
        return round(self.product.calories_per_100g * self.grams / 100)

    @property
    def protein(self):
        return round(float(self.product.protein_per_100g) * self.grams / 100, 1)

    @property
    def fat(self):
        return round(float(self.product.fat_per_100g) * self.grams / 100, 1)

    @property
    def carbs(self):
        return round(float(self.product.carbs_per_100g) * self.grams / 100, 1)