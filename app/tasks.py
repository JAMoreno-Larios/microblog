"""
tasks.py

We set up functions to be sent to the Celery queue
"""

from flask import current_app, render_template
from celery import shared_task
import time
from app.models import db, Task, User, Post
from app.email import send_email
import sys
import sqlalchemy as sa
import json
from celery.result import AsyncResult
from celery.contrib import rdb


# """
# We need to initialize a Flask application since we will be running this
# in a separate process.
# """
# app = create_app()
# app.app_context().push()


def _set_task_progress(celery_task, progress):
    try:
        celery_task.update_state(state='PROGRESS',
                                 meta={'current': progress}
                                 )

        task = db.session.get(Task, celery_task.request.id)
        task.user.add_notification(
            'task_progress',
            {
                'task_id': celery_task.request.id,
                'progress': progress
            }
        )
        if progress >= 100:
            task.complete = True
        db.session.commit()
    except Exception:
        task.complete = True
        db.session.commit()


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


# Implement the Export task
@shared_task(bind=True)
def export_posts(self, user_id):
    try:
        # read user posts
        user = db.session.get(User, user_id)
        _set_task_progress(self, 0)
        data = []
        counter = 0
        total_posts = db.session.scalar(
                sa.select(
                    sa.func.count()
                ).select_from(
                    user.posts.select().subquery()
                )
        )
        for post in db.session.scalars(
            user.posts.select().order_by(
                Post.timestamp.asc()
                )
        ):
            data.append({'body': post.body,
                        'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            counter = counter + 1
            _set_task_progress(self, (100 * counter) // total_posts)
        # send email
        send_email(
            '[Microblog] Your blog posts',
            sender=current_app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html', user=user),
            attachments=[('posts.json', 'application/json',
                          json.dumps({'posts': data}, indent=4))],
            sync=True)

    except Exception:
        # Handle exceptions
        _set_task_progress(self, 100)
        current_app.logger.error('Unhandled exception',
                                 exc_info=sys.exc_info())
    finally:
        _set_task_progress(self, 100)
