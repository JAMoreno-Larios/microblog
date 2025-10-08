"""
Microblog API blueprint
"""

from flask import Blueprint
from .users import users_bp
from .errors import error_bp
from .tokens import token_bp


# Define the parent blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register the childern blueprints here
api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(error_bp)
api_bp.register_blueprint(token_bp)
