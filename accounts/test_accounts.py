import pytest
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse

from .forms import mark_required_labels
from .models import CustomUser


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="petya",
        email="petya@example.com",
        phone="+79990000001",
        password="StrongPass123!",
    )


@pytest.fixture
def friend(django_user_model):
    return django_user_model.objects.create_user(
        username="vasya",
        email="vasya@example.com",
        phone="+79990000002",
        password="StrongPass123!",
    )


def test_mark_required_labels_adds_suffix_for_required_and_optional_fields():
    class DemoForm(forms.Form):
        required_name = forms.CharField(label="Имя", required=True)
        optional_nick = forms.CharField(label="Ник", required=False)

    form = DemoForm()
    mark_required_labels(form)

    assert form.fields["required_name"].label == "Имя (обязательно)"
    assert form.fields["optional_nick"].label == "Ник (необязательно)"


@pytest.mark.django_db
def test_register_view_creates_user_and_redirects_home(client):
    response = client.post(
        reverse("accounts:register"),
        data={
            "username": "new_user",
            "first_name": "Новый",
            "last_name": "Пользователь",
            "email": "new_user@example.com",
            "phone": "+79991112233",
            "age": 21,
            "height": 180,
            "weight": "75.50",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:home")
    assert CustomUser.objects.filter(username="new_user").exists()


@pytest.mark.django_db
def test_profile_detail_denies_access_for_non_friend(client, user, friend):
    client.force_login(user)

    response = client.get(reverse("accounts:profile_detail", kwargs={"username": friend.username}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_add_friend_view_adds_user_to_friends(client, user, friend):
    client.force_login(user)

    response = client.get(reverse("accounts:add_friend", kwargs={"username": friend.username}))

    assert response.status_code == 302
    assert response.url == reverse("accounts:profile_detail", kwargs={"username": friend.username})
    assert user.friends.filter(pk=friend.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query, expected_usernames",
    [
        ("vas", ["vasya"]),
        ("petya@example.com", ["petya"]),
        ("missing", []),
    ],
)
def test_users_list_search_filters_users(client, user, friend, query, expected_usernames):
    client.force_login(user)

    response = client.get(reverse("accounts:users_list"), {"q": query})

    usernames = [u.username for u in response.context["users"]]
    assert response.status_code == 200
    assert usernames == expected_usernames


@pytest.mark.django_db
def test_custom_user_phone_validator_raises_validation_error():
    bad_user = CustomUser(
        username="broken_phone",
        email="broken@example.com",
        phone="abc",
    )

    with pytest.raises(ValidationError):
        bad_user.full_clean()
