"""
Seralizers for user
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


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
