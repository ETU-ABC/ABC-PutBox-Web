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

# Import module models (i.e. Album)
from putbox.albums.models import Album

# Marshmallow schemas for users
from putbox.auth.schemas import user_schema, users_schema

# Import auth service
from putbox.auth.AuthService import Auth



# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET'])
def login_page():
    return render_template('Login.html')


@mod_auth.route('/register', methods=['GET'])
def register_page():
    return render_template('Register.html')


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
    return make_response('Password is incorrect', 401)


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


# Configuration for user settings
mod_user = Blueprint('user', __name__, url_prefix="/user")


# define endpoint for configuration settings
@mod_user.route('/settings', methods=['GET'])
@Auth.token_required
def user_settings(current_user):
    time_to_delete = current_user.auto_delete_time
    # TODO make sure the template page exists
    # returns -1 if not set explicitly
    # front end must handle this
    return render_template("Settings.html", time_to_delete=time_to_delete)


@mod_user.route('/settings', methods=['POST'])
@Auth.token_required
def update_user_settings(current_user):

    time_input = 0
    if 'time_to_auto_del' in request.json:
        time_input = request.json['time_to_auto_del']

    # TODO check if time_input is number

    if time_input.isnumeric() and time_input > 0:
        current_user.auto_delete_time = time_input
        db.session.commit()

    else:
        return "time_input should be positive value"




    return current_user

