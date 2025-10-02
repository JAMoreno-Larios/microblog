"""
Configuration file.
We declare environment variables that are processed
with python-dotenv
"""

import os
from dataclasses import dataclass
basedir = os.path.abspath(os.path.dirname(__file__))


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

    def __class_getitem__(self, item):
        # Makes our class subscriptable
        return getattr(self, item)
