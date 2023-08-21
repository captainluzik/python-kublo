"""
Views for user
"""

from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """represents user creating in System"""
    serializer_class = UserSerializer
