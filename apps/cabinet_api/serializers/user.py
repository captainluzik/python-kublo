from rest_framework import serializers

from apps.cabinet_api.models import CustomUser, PersonalAccount


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


class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAccount
        fields = (
            'id', 'full_name', 'partner_code', 'investment_sector', 'deposit_term', 'total_deposit_amount',
            'interest_rate', 'dividend_amount', 'partners',
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
