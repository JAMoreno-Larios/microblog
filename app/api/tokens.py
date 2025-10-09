"""
API tokens for authentication subsystem
"""
from flask import Blueprint
from app.models import db
from .auth import basic_auth, token_auth

# This blueprint will be nested into api
token_bp = Blueprint('tokens', __name__, url_prefix='/tokens')


@token_bp.route('/', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}


@token_bp.route('/', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
