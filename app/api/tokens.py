"""
API tokens for authentication subsystem
"""
from flask import Blueprint
from app.models import db
from .auth import basic_auth

# This blueprint will be nested into api
token_bp = Blueprint('tokens', __name__, url_prefix='/tokens')


@token_bp.route('/', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}


def revoke_token():
    pass
