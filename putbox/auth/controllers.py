# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  jsonify, g, session, redirect, make_response
# Current app for getting the cookie SECRET_KEY
from flask import current_app as app

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from putbox import db

# Import jwt (json web token)
import jwt

# Import module models (i.e. User)
from putbox.auth.models import Users

# Marshmallow schemas for users
from putbox.auth.schemas import user_schema, users_schema

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = Users.query.filter_by(username=username).first()

    if not user:
        return make_response('User not found', 401)
    if check_password_hash(user.password, password):
        token = jwt.encode({'userid': user.user_id}, app.config['SECRET_KEY'])
        out = jsonify(success=True)
        out.set_cookie('token', token)
        return out
    return make_response('Username or password is incorrect', 401)


# endpoint to create new user
@mod_auth.route('/signup', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(username, email, hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)