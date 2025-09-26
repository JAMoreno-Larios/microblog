"""
Microblog initialization file
"""

from flask import Flask
from config import Config
from flask_migrate import Migrate
from .routes import routes_bp
from .models import db, User, Post


# Initialize extensions outside the application factory
migrate = Migrate()

def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(routes_bp)
    return app
