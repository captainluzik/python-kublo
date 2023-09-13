from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser, PersonalCabinet, InvestmentSector


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, validators=[validate_password], required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    partnership_code = serializers.CharField(required=True)
    investment_sector = serializers.ChoiceField(choices=InvestmentSector.objects.values_list('sector', flat=True),
                                                required=True)
    deposit_term = serializers.DateField(required=True)
    interest_rate = serializers.DecimalField(required=True, max_digits=9, decimal_places=5)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name',
            'last_name', 'partnership_code',
            'investment_sector', 'deposit_term',
            'interest_rate', 'password',
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
                raise serializers.ValidationError(
                    {'email': "Current email is invalid or already taken!"}
                )
            return res
        return res

    def save(self, **kwargs) -> object:

        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({'password': "Passwords must match!"})

        user = CustomUser.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )

        PersonalCabinet.objects.create(
            user=user,
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            partnership_code=self.validated_data['partnership_code'],
            investment_sector=self.validated_data['investment_sector'],
            deposit_term=self.validated_data['deposit_term'],
            interest_rate=self.validated_data['interest_rate'],
        )

        return user


class AllInvestorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCabinet
        fields = "__all__"


class CabinetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCabinet
        fields = [
            'partnership_code',
            'investment_sector',
            'deposit_term'
        ]
