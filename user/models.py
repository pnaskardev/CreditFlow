
import uuid
from django.db import models

class CustomerManager(models.Manager):
    def create(self, **kwargs):
        # Perform custom validation logic here
        email = kwargs.get('email')
        name=kwargs.get('name')
        annual_income=kwargs.get('annual_income')
        adhaar_id=kwargs.get('adhaar_id')
        if not email:
            raise ValueError("User must have an email address")
        if annual_income is None or annual_income < 0:
            raise ValueError("Annual income must be a non-negative value")
        if not name:
            raise ValueError("User must have a name")
        if not adhaar_id:
            raise ValueError("User must have an aadhar id")

        return super().create(**kwargs)

class Customer(models.Model):
    adhaar_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    name = models.CharField(max_length=30)
    annual_income = models.IntegerField(
        default=0, verbose_name='Annual Income')

    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['adhaar_id','name', 'annual_income', ]

    objects = CustomerManager()

    def __str__(self):
        return self.email
