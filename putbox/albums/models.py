# Import the database object (db) from the main application module
from putbox import db, ma
from flask_marshmallow import Schema


class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # TODO album cover is set to first photo in the album
    # cover = db.Column(Integer, ForeignKey('photo.photo_id'))
    photos = db.relationship("Photo")

    def __init__(self, album_name, owner):
        self.album_name = album_name
        self.owner = owner
