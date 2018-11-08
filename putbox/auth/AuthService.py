from functools import wraps
from flask import request, jsonify
import jwt
from putbox.auth.models import Users
from putbox import app


class Auth():
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'token' in request.cookies:
                token = request.cookies.get('token')

            if not token:
                return jsonify({'message' : 'Token is missing!'}), 401

            try:
                user_id = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = Users.query.filter_by(user_id=user_id).first()
                return f(current_user, *args, **kwargs)
            except jwt.ExpiredSignature:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'

        return decorated
