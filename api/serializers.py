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
    password_confirm = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'date_joined', 'is_active',)
        read_only_fields = ('id', 'first_name', 'last_name', 'date_joined', 'is_active',)

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return CustomUser.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")

        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # assign token
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
