"""
tasks.py

We set up functions to be sent to the Celery queue
"""

from flask import current_app
from celery import shared_task
import time


@shared_task(bind=True)
def example(self, seconds):
    print('Starting task')
    for i in range(seconds):
        self.update_state(state='PROGRESS',
                          meta={'current': 100.0 * i / seconds,
                                'total': 100}
                          )
        print(i)
        time.sleep(1)
    print("Task completed")
