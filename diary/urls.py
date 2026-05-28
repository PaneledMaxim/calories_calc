from django.urls import path
from .views import diary_view, add_food_entry_view, delete_food_entry_view

app_name = 'diary'

urlpatterns = [
    path('', diary_view, name='diary'),
    path('add/', add_food_entry_view, name='add'),
    path('<int:entry_id>/delete/', delete_food_entry_view, name='delete_entry'),
    path('<slug:username>/', diary_view, name='friend_diary'),
]