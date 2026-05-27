from django.contrib import admin
from django.urls import path, include

handler404 = "accounts.views.custom_page_not_found"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('diary/', include('diary.urls')),
]
