import time
from celery import shared_task

@shared_task
def run_slow():
    time.sleep(10)