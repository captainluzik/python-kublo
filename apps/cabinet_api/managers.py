from django.contrib.auth.models import UserManager
from rest_framework import serializers


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if self.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email must be unique"})
        return super()._create_user(username, email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        return super().create_user(email, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)
