"""
Microblog initialization file
"""

from flask import Flask, request
from config import Config
from flask_migrate import Migrate
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from .routes import routes_bp
from app.errors import errors_bp
from app.auth import auth_bp
from .models import db, login, User, Post
from .email import mail
from .cli import translate_bp
from .translate import translate


# Instantiate extensions outside the application factory
migrate = Migrate()
moment = Moment()
babel = Babel()


# Define a function to get the locales
def get_locale():
    return request.accept_languages.best_match(Config['LANGUAGES'])


# Define the application factory
def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    # Register blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(translate_bp)
    # Force users to login when viewing protected pages
    login.login_view = 'auth.login'
    login.login_message = _l('Please log in to access this page.')

    """
    The following block enables logging when running without
    debug mode.

    First section enables email logging for errors; second,
    logs to a text file.
    """
    if not app.debug:
        # Email configuration
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD']
                )
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(
                        app.config['MAIL_SERVER'],
                        app.config['MAIL_PORT']
                    ),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Microblog Failure',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Logging to a file
        # Checks if file exists; if not, we create one
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app
