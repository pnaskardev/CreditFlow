from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import os 
from django.db import transaction
from celery.result import AsyncResult

from . tasks import calculate_credit_score

from .models import Customer

@receiver(post_save, sender=Customer)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(instance)

        # task_result = calculate_credit_score.delay(instance.adhaar_id)

        # # Assuming you want to wait for the task to complete and get the result
        # result = AsyncResult(task_result.id)

        # if result.status == 'SUCCESS':
        #     credit_score = result.get()
        #     print(f"Credit score calculated: {credit_score}")
        # else:
        #     print(f"Task status: {result.status}")
        #     print(f"Task did not complete successfully or is still running.")