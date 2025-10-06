"""
tasks.py

We set up functions to be sent to the Celery queue
"""

from flask import current_app
from celery import shared_task
import time


@shared_task
def example(seconds):
    print('Starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print("Task completed")
