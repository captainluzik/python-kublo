from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models, transaction
from django.utils.crypto import get_random_string

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

    def generate_unique_partner_code(self):
        """Method to make sure that generated random string is unique"""
        with transaction.atomic():
            partner_code = get_random_string(10)
            while PersonalAccount.objects.filter(partner_code=partner_code).exists():
                partner_code = get_random_string(10)
            PersonalAccount.objects.create(partner_code=partner_code)
            return partner_code

    def save(self, *args, **kwargs):
        """Method override to create personal account model instance too"""
        super().save(*args, **kwargs)

        # check if user already have personal account and create one if it doesn't exist
        if not hasattr(self, 'account'):
            PersonalAccount.objects.create(
                user=self,
                partner_code=self.generate_unique_partner_code(),
                investment_sector="Default Sector",
            )


class PersonalAccount(models.Model):
    INVESTMENT_SECTOR_CHOICES = [
        ('informational_technologies', 'Informational Technologies'),
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('financials', 'Financials'),
        ('consumer', 'Consumer'),
        ('industrials', 'Industrials'),

    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    partner_code = models.CharField(max_length=10, unique=True, validators=[
        validators.MinLengthValidator(10, message="Partner code has to be exactly 10 characters long"),
    ])
    investment_sector = models.CharField(max_length=50, choices=INVESTMENT_SECTOR_CHOICES)
    deposit_term_start = models.DateField(null=True, help_text="Start date of investment term")
    deposit_term_end = models.DateField(null=True, help_text="End date of investment term")
    total_deposit_amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dividend_amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)

    partners = models.ManyToManyField(CustomUser, related_name='partner', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=('partner_code',))
        ]

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def deposit_term_duration(self):
        return self.deposit_term_end - self.deposit_term_start \
            if self.deposit_term_start and self.deposit_term_end else None

    def __str__(self):
        return f'{self.user.email} - {self.investment_sector}'
