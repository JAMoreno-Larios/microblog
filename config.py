"""
Configuration file.
We declare environment variables that are processed
with python-dotenv
"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass
basedir = os.path.abspath(os.path.dirname(__file__))

# Load additional environmental variables
load_dotenv()


@dataclass
class Config:
    """
    Configuration class for our Flask app
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adivina-adivinador'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(
        basedir, 'app.db')
    # Add email support
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['agustin90m@gmail.com']

    # Pagination
    POSTS_PER_PAGE = 25

    # Supported languages via Flask-Babel
    LANGUAGES = ['en', 'es']

    # Microsoft translator API key
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    MS_TRANSLATOR_LOCATION = os.environ.get('MS_TRANSLATOR_LOCATION')

    # Elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Celery
    CELERY = dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
        task_track_started=True
    )

    def __class_getitem__(self, item):
        # Makes our class subscriptable
        return getattr(self, item)
