"""
errors.py
Error handlers for our Microblog
"""

from flask import Blueprint, render_template
from .models import db

# Define blueprint
errors_bp = Blueprint('errors', __name__)

"""
We use app_errorhandler() since it can handle errors for every request.
Page errors occur at the routing level before the blueprint can be
determined.
"""


# Page not found
@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# Internal server error
@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
