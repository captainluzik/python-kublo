from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('account/', views.UserRetrieveUpdateAPIView.as_view(), name='account'),
    path('account/<int:pk>', views.AdminUserRetrieveUpdateAPIView.as_view(), name='admin-account'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
