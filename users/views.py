from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user with username + password (+ optional email).

    Example body:
    {
        "username": "kavi",
        "password": "password123",
        "email": "kavi@example.com"  // optional
    }
    """
    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Username already taken"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    tokens = get_tokens_for_user(user)

    return Response(
        {
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": tokens,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login with EITHER username OR user id + password.

    Example bodies:

    {
        "identifier": "kavi",
        "password": "password123"
    }

    OR:

    {
        "identifier": "3",  // user with id=3
        "password": "password123"
    }

    You can also send "username" or "id" instead of "identifier".
    """
    identifier = (
        request.data.get("identifier")
        or request.data.get("username")
        or request.data.get("id")
    )
    password = request.data.get("password")

    if not identifier or not password:
        return Response(
            {"detail": "Identifier and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = None
    UserModel = get_user_model()

    # 1) If identifier looks like an integer, try to treat it as user ID
    if str(identifier).isdigit():
        try:
            candidate = UserModel.objects.get(pk=int(identifier))
        except UserModel.DoesNotExist:
            candidate = None

        if (
            candidate is not None
            and candidate.is_active
            and candidate.check_password(password)
        ):
            user = candidate

    # 2) If we still don't have a user, try username-based authenticate
    if user is None:
        # authenticate uses USERNAME_FIELD; for default User that is "username"
        user = authenticate(request, username=identifier, password=password)

    if user is None or not user.is_active:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    tokens = get_tokens_for_user(user)

    return Response(
        {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": tokens,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Simple protected endpoint to verify JWT auth is working.

    Call with:
      Authorization: Bearer <access_token>
    """
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": getattr(user, "email", None),
        },
        status=status.HTTP_200_OK,
    )
