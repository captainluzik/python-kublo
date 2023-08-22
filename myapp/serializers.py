from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True,
                         'validators': [validate_password]}
        }

    def is_valid(self, *, raise_exception=False) -> bool:
        res = super().is_valid()
        if not res:
            if 'email' in self.errors:
                raise serializers.ValidationError({'email': "Current email is invalid or already taken!"})
            return res
        return res

    def save(self, **kwargs) -> object:

        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({'password': "Passwords must match!"})

        user = CustomUser.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )

        return user
