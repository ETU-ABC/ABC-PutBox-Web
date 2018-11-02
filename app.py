from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
import os
import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bil495-abc.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    register_date = db.Column(db.DateTime)
    albums = relationship('Album')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.register_date = datetime.datetime.now()


class UserSchema(ma.Schema):

    class Meta:
        # Fields to expose
        fields = ('user_id', 'username', 'email', 'register_date')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    photo_path = db.Column(db.String(150), unique=True)
    upload_date = db.Column(db.DateTime)
    uploaded_by = db.Column(Integer, ForeignKey('user.user_id'))
    tags = relationship("Tag")
    album_id = db.Column(Integer, ForeignKey('album.album_id'))

    def __init__(self, photo_path, uploaded_by):
        self.photo_path = photo_path
        self.uploaded_by = uploaded_by
        self.upload_date = datetime.datetime.now()


class PhotoSchema(ma.Schema):

    class Meta:
        fields = ('photo_id', 'photo_path', 'upload_date', 'uploaded_by', 'tags')
    tags = ma.Nested('TagSchema', many=True, only='tag_desc')


photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(Integer, ForeignKey('photo.photo_id'))
    tag_desc = db.Column(db.String(50))

    def __init__(self, photo_id, tag_desc):
        self.photo_id = photo_id
        self.tag_desc = tag_desc


class TagSchema(ma.Schema):
    class Meta:
        fields = ('photo_id', 'tag_desc')
        # only = 'tag_desc'


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(30), unique=True)
    owner = db.Column(Integer, ForeignKey('user.user_id'))
    # TODO album cover is set to first photo in the album
    # cover = db.Column(Integer, ForeignKey('photo.photo_id'))
    photos = relationship("Photo")

    def __init__(self, album_name, owner):
        self.album_name = album_name
        self.owner = owner


class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('album_name', 'owner', 'photos')
    photos = ma.Nested('PhotoSchema', many=True)


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_user = User(username, email, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to insert new photo
@app.route("/photo", methods=["POST"])
def add_photo():
    photo_path = request.json['photo_path']
    # TODO update after user authentication
    uploaded_by = 1

    new_photo = Photo(photo_path, uploaded_by)

    db.session.add(new_photo)
    db.session.commit()

    return photo_schema.jsonify(new_photo)


# endpoint to show all photos
@app.route("/photo", methods=["GET"])
def get_photo():
    all_photos = Photo.query.all()
    result = photos_schema.dump(all_photos)
    return photos_schema.jsonify(result.data)


if __name__ == '__main__':
    app.run(debug=True)
    
