"""
errors/handlers.py
Error handlers for our Microblog
"""

from flask import Blueprint, render_template, request
from app.models import db
from app.api.errors import error_response as api_error_response

# Define blueprint
errors_bp = Blueprint('errors', __name__,
                      template_folder='templates')

# Content negotiation for error responses.
def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

"""
We use app_errorhandler() since it can handle errors for every request.
Page errors occur at the routing level before the blueprint can be
determined.
"""


# Page not found
@errors_bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


# Internal server error
@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
