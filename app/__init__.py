"""
Microblog initialization file
"""

from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes import routes_bp

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# from app import routes, models  # Prevents circular import

# Initialize extensions outside the application factory
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(routes_bp)
    # import .models
    return app
