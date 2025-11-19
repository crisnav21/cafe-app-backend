from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Product


def get_demo_user():
    user, _ = User.objects.get_or_create(
        username="demo_user", defaults={"email": "demo@example.com"}
    )
    return user


@api_view(["GET"])
def cart_list(request):
    user = get_demo_user()
    items = CartItem.objects.filter(user=user)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def cart_add(request):
    user = get_demo_user()
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(
            {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        defaults={"quantity": quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()

    serializer = CartItemSerializer(item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def cart_remove(request, pk):
    user = get_demo_user()
    try:
        item = CartItem.objects.get(pk=pk, user=user)
    except CartItem.DoesNotExist:
        return Response({"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
