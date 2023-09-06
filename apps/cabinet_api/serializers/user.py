from rest_framework import serializers

from apps.cabinet_api.models import CustomUser, PersonalAccount


class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAccount
        fields = (
            'id', 'partner_code', 'investment_sector', 'deposit_term', 'total_deposit_amount',
            'interest_rate', 'dividend_amount', 'partners',
        )


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
    account = PersonalAccountSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'password_confirm',
                  'first_name', 'last_name', 'date_joined', 'is_active', 'account', )
        read_only_fields = ('id', 'date_joined', 'is_active',)

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")

        validated_data.pop('password_confirm')

        # account_data = validated_data.pop('account', {})

        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            # If admin, handle the account data update separately
            account_data = validated_data.pop('account', {})

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            # Update the PersonalAccount associated with the user
            account_instance = instance.account
            for attr, value in account_data.items():
                setattr(account_instance, attr, value)

            account_instance.save()
        else:
            # If not an admin, only update the user data (excluding account data)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance
