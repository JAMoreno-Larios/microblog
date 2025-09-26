"""
Configuration file.
We declare environment variables that are processed
with python-dotenv
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration class for our Flask app
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adivina-adivinador'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(
        basedir, 'app.db')
