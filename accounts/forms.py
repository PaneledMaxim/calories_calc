from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("Пароли не совпадают."),
    }

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": _("Логин"),
            "email": _("Электронная почта"),
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
        }
        help_texts = {
            "username": _(
                "Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."
            ),
            "email": _("Укажите электронную почту."),
            "first_name": _("Укажите имя."),
            "last_name": _("Укажите фамилию."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = _("Пароль")
        self.fields["password2"].label = _("Подтверждение пароля")
        self.fields["password1"].help_text = _(
            "Пароль не должен быть слишком простым и состоять только из цифр."
        )
        self.fields["password2"].help_text = _("Введите тот же пароль еще раз для проверки.")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": _("Логин"),
            "email": _("Электронная почта"),
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
        }
