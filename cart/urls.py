from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list, name="cart-list"),  # GET
    path("add/", views.cart_add, name="cart-add"),  # POST
    path("<int:pk>/", views.cart_remove, name="cart-remove"),  # DELETE
]
