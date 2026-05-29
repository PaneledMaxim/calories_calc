import pytest
from django.urls import reverse

from .models import Product


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="petya",
        email="petya@example.com",
        phone="+79990000001",
        password="StrongPass123!",
    )


@pytest.fixture
def other_user(django_user_model):
    return django_user_model.objects.create_user(
        username="vasya",
        email="vasya@example.com",
        phone="+79990000002",
        password="StrongPass123!",
    )


@pytest.fixture
def product(user):
    return Product.objects.create(
        name="Овсянка",
        calories_per_100g=350,
        protein_per_100g=12,
        fat_per_100g=6,
        carbs_per_100g=60,
        creator=user,
    )


@pytest.mark.django_db
def test_product_list_view_is_available_without_login(client, product):
    response = client.get(reverse("products:list"))

    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_add_product_view_requires_login(client):
    response = client.get(reverse("products:add"))

    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_add_product_view_creates_product_with_creator(client, user):
    client.force_login(user)

    response = client.post(
        reverse("products:add"),
        data={
            "name": "Гречка",
            "calories_per_100g": 310,
            "protein_per_100g": 12.6,
            "fat_per_100g": 3.3,
            "carbs_per_100g": 62,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("products:list")
    created = Product.objects.get(name="Гречка")
    assert created.creator == user


@pytest.mark.django_db
def test_edit_product_view_allows_owner(client, user, product):
    client.force_login(user)

    response = client.post(
        reverse("products:edit", kwargs={"product_id": product.pk}),
        data={
            "name": "Овсянка обновлённая",
            "calories_per_100g": 360,
            "protein_per_100g": 12,
            "fat_per_100g": 6,
            "carbs_per_100g": 60,
        },
    )

    assert response.status_code == 302
    product.refresh_from_db()
    assert product.name == "Овсянка обновлённая"


@pytest.mark.django_db
def test_edit_product_view_denies_other_user(client, other_user, product):
    client.force_login(other_user)

    response = client.get(reverse("products:edit", kwargs={"product_id": product.pk}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_product_view_deletes_for_owner(client, user, product):
    client.force_login(user)

    response = client.post(reverse("products:delete", kwargs={"product_id": product.pk}))

    assert response.status_code == 302
    assert response.url == reverse("products:list")
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_delete_product_view_denies_other_user(client, other_user, product):
    client.force_login(other_user)

    response = client.post(reverse("products:delete", kwargs={"product_id": product.pk}))

    assert response.status_code == 403
    assert Product.objects.filter(pk=product.pk).exists()
