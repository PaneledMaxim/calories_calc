from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    calories_per_100g = models.PositiveIntegerField(verbose_name="Калории на 100г")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name']