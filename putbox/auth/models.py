# Import the database object (db) from the main application module
from putbox import db
from flask_marshmallow import Schema


# Define a User model
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    register_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    albums = db.relationship('Album')
    auto_delete_time = db.Column(db.Integer, default=-1)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class UserSchema(Schema):

    class Meta:
        # Fields to expose
        fields = ('user_id', 'username', 'email', 'register_date')
