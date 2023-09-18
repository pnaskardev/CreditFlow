from django.db.models.signals import post_save
from django.dispatch import receiver
from . utils import calculate_emi_due_dates

from .models import LoanApplication, EMI

@receiver(post_save,sender=LoanApplication)
def create_profile(sender, instance, created, **kwargs):
    print(instance.id)