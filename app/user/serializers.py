"""
Seralizers for user
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """represents serializer for user"""

    class Meta:
        """represents rules for password and
        fields for user needed"""
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {
            'write_only': True,
            'min_length': 5
        }}

    def create(self, validated_data):
        """creates user with encrypted pass"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(TokenObtainPairSerializer):
    """represents serializer for user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """validates and authenticate the user"""
        user = super().validate(attrs)
        attrs['user'] = user
        return attrs
