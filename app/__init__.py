"""
Microblog initialization file
"""

from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from .routes import routes_bp
from .models import db, User, Post


# Instantiate extensions outside the application factory
migrate = Migrate()
login = LoginManager()


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
    return app
