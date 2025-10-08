"""
User API definitions
"""

from Flask import Blueprint

# This blueprint will be nested into api
users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('<int_id>', methods=['GET'])
def get_user(id):
    pass


@users_bp.route('/', methods=['GET'])
def get_users():
    pass


@users_bp.route('<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass


@users_bp.route('<int:id>/following', methods=['GET'])
def get_following(id):
    pass


@users_bp.route('/', methods=['POST'])
def create_user():
    pass


@users_bp.route('<int:id>', methods=['PUT'])
def update_user(id):
    pass
