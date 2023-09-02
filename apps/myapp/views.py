from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Registration a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING,
                                           format="password", min_length=8
                                           ),
                "password2": openapi.Schema(
                    title="Password confirmation", type=openapi.TYPE_STRING,
                    format="password", min_length=8
                ),
            },
            required=["email", "password", "password2"],
        ),
        responses={201: "Registration is successful", 400: "Bad request - Validation errors!"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        data = {}
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user."

            refresh_token = RefreshToken.for_user(user)
            data['refresh'] = str(refresh_token)
            data['access'] = str(refresh_token.access_token)

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Token pair getter",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING,
                                           format="password", min_length=8
                                           )
            },
            required=["email", "password"],
        ),
        responses={200: "OK",
                   401: "No active account found with the given credentials"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        user = authenticate(email=request.data['email'],
                            password=request.data['password'])
        if user is not None:
            login(request, user)
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(jwt_views.TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Token pair refresher",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING,
                                           format="password", min_length=8
                                           )
            },
            required=["email", "password"],
        ),
        responses={200: "OK",
                   401: "No active account found with the given credentials"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)

