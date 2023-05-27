import re
from flask import g, make_response, jsonify


def verify_password_user(name_or_token, password):
    from ..models import User
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    user = User.verify_auth_token(name_or_token)
    if not user:
        user = User.query.filter_by(name=name_or_token).first()
        if user is None or not user.verify_password(password):
            return False
    g.user = user
    return True


def verify_password_admin(name_or_token, password):
    from ..models import Admin
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if admin is None:
        admin = Admin.query.filter_by(name=name_or_token).first()
        if admin is None or not admin.verify_password(password):
            return False
    g.admin = admin
    return True


def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
