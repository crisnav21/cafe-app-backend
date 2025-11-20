from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product-list"),  # /api/products/
    path("<int:pk>/", views.product_detail, name="product-detail"),  # /api/products/1/
]
