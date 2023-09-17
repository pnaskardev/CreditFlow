import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, adhaar_id,email, name, annual_income,  **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")
        if not annual_income:
            raise ValueError("User must have an annual income")
        if not adhaar_id:
            raise ValueError("User must have an aadhar id")

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            annual_income=annual_income,
            adhaar_id=adhaar_id,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, adhaar_id,email, name, annual_income, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            annual_income=annual_income,
            adhaar_id=adhaar_id,
            **extra_fields
        )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    adhaar_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    name = models.CharField(max_length=30)
    annual_income = models.IntegerField(
        default=0, verbose_name='Annual Income')

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['adhaar_id','name', 'annual_income', ]

    objects = UserManager()

    def __str__(self):
        return self.email
