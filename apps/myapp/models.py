from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, MinValueValidator, MinLengthValidator
from django.db import models

from datetime import date, datetime


def date_validator(date_to_validate: date) -> None:
    if date_to_validate <= datetime.now().date():
        raise ValidationError("The date must be greater than today!")


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email: str = None,
                    password: str = None) -> object:
        if not email:
            raise ValidationError("The Email field is required!")

        if "@" not in email or "." not in email:
            raise ValidationError("Invalid email format!")

        if not password:
            raise ValidationError("The Password field is required!")

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,
                         email: str = None,
                         password: str = None) -> object:
        if not email:
            raise ValidationError("The Email field is required!")

        if "@" not in email or "." not in email:
            raise ValidationError("Invalid email format!")

        if not password:
            raise ValidationError("The Password field is required!")

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.CharField(max_length=255, null=False, unique=True,
                             blank=False, validators=[validate_email])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    class Meta:
        app_label = 'myapp'

    @staticmethod
    def has_perm(perm, obj=None) -> bool:
        return True

    @staticmethod
    def has_module_perms(app_label) -> bool:
        return True

    @property
    def is_staff(self) -> models.BooleanField:
        return self.is_admin


class PersonalCabinet(models.Model):
    user = models.OneToOneField(CustomUser, related_name="cabinet", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, validators=[
        MinLengthValidator(2, message="First name characters number should be greater than 2!")])
    last_name = models.CharField(max_length=255, validators=[
        MinLengthValidator(2, message="Last name characters number should be greater than 2!")])
    partnership_code = models.CharField(max_length=100, unique=True, validators=[
        MinLengthValidator(3, message="Partnership code characters number should be greater than 3!")])
    investment_sector = models.CharField(max_length=100, validators=[
        MinLengthValidator(2, message="Investment sector characters number should be greater than 2!")])
    deposit_term = models.DateField(validators=[date_validator])
    interest_rate = models.DecimalField(max_digits=9, decimal_places=5, validators=[
        MinValueValidator(0, message="Interest rate should be greater than 0!")])

    @property
    def referral_partners_list(self):
        return list()

    @property
    def total_deposit_amount(self):
        return float(0)

    @property
    def received_dividends_amount(self):
        return float(0)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name
