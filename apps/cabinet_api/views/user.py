from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.cabinet_api.serializers import UserRegisterSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        operation_description="User registration endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email", pattern=r"^[\w.@+-]+$"
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING, format="password", min_length=8),
                "password2": openapi.Schema(
                    title="Password confirm", type=openapi.TYPE_STRING, format="password", min_length=8
                ),
            },
            required=["email", "password", "password2"],
        ),
        responses={201: "JWT keys pair for user", 400: "Bad request - Validation errors"},
    )
    def post(self, request, *args, **kwargs):
        user_serializer = UserRegisterSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.save()
        refresh_token = RefreshToken.for_user(user)
        data = {"refresh": str(refresh_token), "access": str(refresh_token)}
        return Response(data, status=status.HTTP_201_CREATED)
