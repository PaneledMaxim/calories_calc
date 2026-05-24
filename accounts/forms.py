from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


def mark_required_labels(form):
    for field in form.fields.values():
        if field.required:
            field.label = f"{field.label} (обязательно)"
        else:
            field.label = f"{field.label} (необязательно)"


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["username"].label = "Логин"
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Электронная почта"
        self.fields["phone"].label = "Телефон"
        self.fields["age"].label = "Возраст"
        self.fields["height"].label = "Рост, см"
        self.fields["weight"].label = "Вес, кг"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"
        mark_required_labels(self)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "age",
            "height",
            "weight",
        )


class CustomUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Электронная почта"
        self.fields["phone"].label = "Телефон"
        self.fields["age"].label = "Возраст"
        self.fields["height"].label = "Рост, см"
        self.fields["weight"].label = "Вес, кг"

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "age", "height", "weight")
