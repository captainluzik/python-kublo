from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email: str = None,
                    password: str = None) -> object:
        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,
                         email: str = None,
                         password: str = None) -> object:
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
