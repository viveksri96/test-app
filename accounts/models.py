from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('Valid phone number needed.')
        user = self.model(phone_number=phone_number)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, **extra_fields):
        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, null=False, unique=True)
    password = None
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []



