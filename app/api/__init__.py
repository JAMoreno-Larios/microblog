"""
Microblog API blueprint
"""

from flask import Blueprint
from .users import users_bp


# Define the parent blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register the childern blueprints here
api_bp.register_blueprint(users_bp)
