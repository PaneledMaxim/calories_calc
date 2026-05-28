from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    calories_per_100g = models.PositiveIntegerField(verbose_name="Калории на 100г")
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Белки на 100г")
    fat_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Жиры на 100г")
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Углеводы на 100г")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Создатель")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name']