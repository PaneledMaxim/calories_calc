from django.urls import path
from .views import diary_view, add_food_entry_view

app_name = 'diary'

urlpatterns = [
    path('', diary_view, name='diary'),
    path('add/', add_food_entry_view, name='add'),
]