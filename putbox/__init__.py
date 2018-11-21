# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask-marshmallow for serializing/deserializing
from flask_marshmallow import Marshmallow

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Sample HTTP error handling
# @app.errorhandler(404)
def not_found(error):
    # return render_template('404.html'), 404
    return render_template('Login.html')

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module
from putbox.auth.controllers import mod_auth as auth_module
from putbox.photos.controllers import mod_photo as photo_module
from putbox.albums.controllers import mod_album as album_module
from putbox.auth.controllers import mod_user as user_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(photo_module)
app.register_blueprint(album_module)
app.register_blueprint(user_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
