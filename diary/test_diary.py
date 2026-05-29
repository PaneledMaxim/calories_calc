import pytest
from django.urls import reverse

from products.models import Product

from .models import FoodEntry


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


@pytest.fixture
def product(user):
    return Product.objects.create(
        name="Яблоко",
        calories_per_100g=50,
        protein_per_100g=0.3,
        fat_per_100g=0.2,
        carbs_per_100g=14,
        creator=user,
    )


@pytest.fixture
def food_entry(user, product):
    return FoodEntry.objects.create(
        user=user,
        product=product,
        grams=200,
        meal_type="breakfast",
    )


@pytest.mark.django_db
def test_food_entry_calories_property(product, user):
    entry = FoodEntry.objects.create(
        user=user,
        product=product,
        grams=200,
        meal_type="lunch",
    )

    assert entry.calories == 100


@pytest.mark.django_db
def test_diary_view_requires_login(client):
    response = client.get(reverse("diary:diary"))

    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_diary_view_shows_totals_for_own_entries(client, user, food_entry):
    client.force_login(user)

    response = client.get(reverse("diary:diary"))

    assert response.status_code == 200
    assert response.context["total_calories"] == 100
    assert response.context["is_own_diary"] is True


@pytest.mark.django_db
def test_friend_diary_view_allows_friend(client, user, friend, food_entry):
    friend.friends.add(user)
    client.force_login(friend)

    response = client.get(reverse("diary:friend_diary", kwargs={"username": user.username}))

    assert response.status_code == 200
    assert response.context["viewed_user"] == user
    assert response.context["total_calories"] == 100


@pytest.mark.django_db
def test_friend_diary_view_denies_non_friend(client, user, friend, food_entry):
    client.force_login(friend)

    response = client.get(reverse("diary:friend_diary", kwargs={"username": user.username}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_add_food_entry_view_creates_entry(client, user, product):
    client.force_login(user)

    response = client.post(
        reverse("diary:add"),
        data={
            "product": product.pk,
            "grams": 150,
            "meal_type": "dinner",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("diary:diary")
    entry = FoodEntry.objects.get(user=user, product=product)
    assert entry.grams == 150
    assert entry.meal_type == "dinner"


@pytest.mark.django_db
def test_delete_food_entry_view_deletes_own_entry(client, user, food_entry):
    client.force_login(user)

    response = client.get(reverse("diary:delete_entry", kwargs={"entry_id": food_entry.pk}))

    assert response.status_code == 302
    assert not FoodEntry.objects.filter(pk=food_entry.pk).exists()


@pytest.mark.django_db
def test_delete_food_entry_view_denies_other_user(client, friend, food_entry):
    client.force_login(friend)

    response = client.get(reverse("diary:delete_entry", kwargs={"entry_id": food_entry.pk}))

    assert response.status_code == 403
    assert FoodEntry.objects.filter(pk=food_entry.pk).exists()
