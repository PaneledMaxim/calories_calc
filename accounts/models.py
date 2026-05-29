from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    email = models.EmailField("Электронная почта", unique=True)
    phone = models.CharField(
        "Телефон",
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[\d\s\-()]{7,20}$",
                message="Введите корректный номер телефона.",
            )
        ],
    )
    age = models.PositiveSmallIntegerField("Возраст", blank=True, null=True)
    height = models.PositiveSmallIntegerField("Рост, см", blank=True, null=True)
    weight = models.DecimalField("Вес, кг", max_digits=5, decimal_places=2, blank=True, null=True)
    friends = models.ManyToManyField("self", blank=True)

    @classmethod
    def searchable(cls):
        """Пользователи, которых можно искать и добавлять в друзья (без админов)."""
        return cls.objects.filter(is_superuser=False, is_staff=False)

    def can_be_added_as_friend(self):
        return not self.is_superuser and not self.is_staff

    def __str__(self):
        return self.username
