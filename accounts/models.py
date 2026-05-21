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
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.username
