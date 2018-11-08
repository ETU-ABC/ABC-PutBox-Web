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

            current_user = validate_token(token)
            if current_user is None:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated
