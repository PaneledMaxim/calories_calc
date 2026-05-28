from django.urls import path
from .views import product_list_view, add_product_view, edit_product_view, delete_product_view

app_name = 'products'

urlpatterns = [
    path('', product_list_view, name='list'),
    path('add/', add_product_view, name='add'),
    path('<int:product_id>/edit/', edit_product_view, name='edit'),
    path('<int:product_id>/delete/', delete_product_view, name='delete'),
]
