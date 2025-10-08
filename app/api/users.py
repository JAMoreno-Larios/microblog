"""
User API definitions
"""

from flask import Blueprint, request, url_for
from app.models import db, User
import sqlalchemy as sa
from .errors import bad_request

# This blueprint will be nested into api
users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('<int:id>', methods=['GET'])
def get_user(id):
    return db.get_or_404(User, id).to_dict()


@users_bp.route('/', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(sa.select(User),
                                   page, per_page,
                                   'api.users.get_users')


@users_bp.route('<int:id>/followers', methods=['GET'])
def get_followers(id):
    user = db.get_or_404(User, id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(user.followers.select(), page, per_page,
                                   'api.users.get_followers', id=id)


@users_bp.route('<int:id>/following', methods=['GET'])
def get_following(id):
    user = db.get_or_404(User, id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return User.to_collection_dict(user.following.select(), page, per_page,
                                   'api.users.get_following', id=id)


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data\
        or 'email' not in data\
            or 'password' not in data:
        return bad_request(
                    "must include username, email and password fields"
            )
    if db.session.scalar(
        sa.select(User).where(
                User.username == data['username']
            )
    ):
        return bad_request('please use a different username')
    if db.session.scalar(
            sa.select(User).where(
                User.email == data['email']
            )
    ):
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201, {'Location': url_for('api.users.get_user',
                                                     id=user.id)}


@users_bp.route('<int:id>', methods=['PUT'])
def update_user(id):
    pass
