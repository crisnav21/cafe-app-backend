from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"message": "Email and password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DEMO: accept any non-empty email & password
    return Response(
        {
            "message": "Login successful",
            "token": "fake-jwt-token-123",  # you can generate real tokens later
            "user": {"email": email},
        }
    )
