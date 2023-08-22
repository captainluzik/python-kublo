"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core import settings

from apps.cabinet_api.views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

static_and_media_urls = [
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("apps.cabinet_api.urls")),
]

urlpatterns += static_and_media_urls
