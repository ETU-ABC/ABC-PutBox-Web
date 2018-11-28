# Import flask and template operators
from flask import Flask, render_template, redirect

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask-marshmallow for serializing/deserializing
from flask_marshmallow import Marshmallow

# Import flask-uploads
from flask_uploads import UploadSet, configure_uploads, IMAGES

# Import heroku
from flask_heroku import Heroku

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static')

# Configurations
app.config.from_object('config')
if app.config['ENV'] == 'production':
    heroku = Heroku(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)

photo_upload = UploadSet('photos', IMAGES)
configure_uploads(app, photo_upload)

# Sample HTTP error handling
# @app.errorhandler(404)
def not_found(error):
    # return render_template('404.html'), 404
    return render_template('Login.html')


# Import views
from putbox.views import *

# Register blueprint(s)
app.register_blueprint(root_module)
app.register_blueprint(auth_module)
app.register_blueprint(photo_module)
app.register_blueprint(album_module)
app.register_blueprint(user_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
