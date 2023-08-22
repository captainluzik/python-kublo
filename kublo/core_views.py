from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt import views as jwt_views


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
    def post(self, request, *args, **kwargs):
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
