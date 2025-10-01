"""
Microblog initialization file
"""

from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from .routes import routes_bp
from .errors import errors_bp
from .models import db, login, User, Post
from .email import mail


# Instantiate extensions outside the application factory
migrate = Migrate()
moment = Moment()


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
    # Register blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(errors_bp)
    # Force users to login when viewing protected pages
    login.login_view = 'routes.login'

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
