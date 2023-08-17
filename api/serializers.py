from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # assign token
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data