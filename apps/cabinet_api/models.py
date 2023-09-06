from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from core import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # remove username field so only email is required to make account
    username = None
    email = models.EmailField(db_index=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class PersonalAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, validators=[
        validators.MinLengthValidator(2, message="First name should be at least 2 characters long"),
    ])
    last_name = models.CharField(max_length=255, validators=[
        validators.MinLengthValidator(2, message="Last name should be at least 2 characters long"),
    ])
    partner_code = models.CharField(max_length=10, unique=True)
    investment_sector = models.CharField(max_length=50, validators=[
        validators.MinLengthValidator(2, message="Investment sector should be at least 2 characters long"),
    ])
    deposit_term = models.DurationField()
    total_deposit_amount = models.DecimalField(max_digits=20, decimal_places=10)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    dividend_amount = models.DecimalField(max_digits=20, decimal_places=10)

    partners = models.ManyToManyField(CustomUser, related_name='partner', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=('partner_code',))
        ]

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.user.email} - {self.investment_sector}'
