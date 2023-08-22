from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.cabinet_api.serializers import TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(responses={200: TokenObtainPairResponseSerializer})  # noqa
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(responses={200: TokenRefreshResponseSerializer})  # noqa
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
