from celery import shared_task

@shared_task
def sharedtask():
    print("Shared task envoked")
    return