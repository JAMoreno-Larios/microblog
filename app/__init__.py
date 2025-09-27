"""
Microblog initialization file
"""

from flask import Flask
from config import Config
from flask_migrate import Migrate
import logging
from logging.handlers import SMTPHandler
from .routes import routes_bp
from .errors import errors_bp
from .models import db, login, User, Post


# Instantiate extensions outside the application factory
migrate = Migrate()


def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
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
    # Enable email logging when the application is running without debug mode
    if not app.debug:
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

    return app
