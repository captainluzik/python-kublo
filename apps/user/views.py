"""
Views for user
"""

from rest_framework import generics
from .serializers import (UserSerializer,
                          AuthTokenSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserView(generics.CreateAPIView):
    """represents user creating in System"""
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    """represents user log-in"""
    serializer_class = AuthTokenSerializer
