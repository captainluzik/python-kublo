from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.cabinet_api.models import CustomUser, PersonalAccount


class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAccount
        fields = (
            'id', 'partner_code', 'investment_sector', 'deposit_term_start', 'deposit_term_end', 'total_deposit_amount',
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
            # Only admin can update fields
            account_data = validated_data.pop('account', {})

            # Update the PersonalAccount associated with the user
            account_instance = instance.account
            for attr, value in account_data.items():
                if attr in ('investment_sector', 'partner_code'):
                    setattr(account_instance, attr, value)
                elif attr == 'deposit_term_end':
                    self._update_deposit_term(account_instance, value)
                else:
                    raise PermissionDenied(f"Admins are not allowed to update field '{attr}'.")

            account_instance.save()
        else:
            raise PermissionDenied("Regular users are not allowed to update this resource.")

        return instance

    def _update_deposit_term(self, instance, new_deposit_term_end):
        deposit_term_start = instance.deposit_term_start
        deposit_term_end = instance.deposit_term_end

        # TODO: maybe deposit duration has to be at least a month
        if deposit_term_start is None:
            # If this is first deposit term for a user
            instance.deposit_term_start = timezone.now().date()
            instance.deposit_term_end = new_deposit_term_end
        else:
            if new_deposit_term_end < deposit_term_start or new_deposit_term_end < timezone.now().date():
                # raise error if provided term shorter than start or current date
                raise ValidationError("Invalid deposit term end date")
            elif deposit_term_end <= timezone.now().date():
                # If this  old deposit term has already ended
                instance.deposit_term_start = timezone.now().date()
                instance.deposit_term_end = new_deposit_term_end
            elif deposit_term_end <= new_deposit_term_end:
                # extend current deposit term or leave it the same if it is equal to current deposit_term_end
                instance.deposit_term_end = new_deposit_term_end
            elif deposit_term_end > new_deposit_term_end:
                # shortening deposit_term_end
                instance.deposit_term_end = new_deposit_term_end
            else:
                raise ValidationError("Unexpected error while updating deposit term.")
