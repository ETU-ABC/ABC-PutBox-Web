# Import the database object (db) from the main application module
from putbox import db


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String, unique=True)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tags = db.relationship("Tag")
    liked_by = db.relationship("Like")
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
    def __init__(self, photo_path, uploaded_by, album_id):
        self.photo_path = photo_path
        self.uploaded_by = uploaded_by
        self.album_id = album_id

class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'))
    liked_by = db.Column(db.String)

    def __init__(self, photo_id, liked_by):
        self.photo_id = photo_id
        self.liked_by = liked_by


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'))
    tag_desc = db.Column(db.String)

    def __init__(self, photo_id, tag_desc):
        self.photo_id = photo_id
        self.tag_desc = tag_desc
