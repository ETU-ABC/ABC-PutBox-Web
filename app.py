from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
import os
import datetime
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bil495-abc.sqlite')
app.config['SECRET_KEY'] = 'etu-abc-putbox'
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
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    tags = relationship("Tag")
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))

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
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'))
    tag_desc = db.Column(db.String(50))

    def __init__(self, photo_id, tag_desc):
        self.photo_id = photo_id
        self.tag_desc = tag_desc


class TagSchema(ma.Schema):
    class Meta:
        fields = ('photo_id', 'tag_desc')


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(30), unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'))
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


#------AUTH------
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


# validate if token is signatured and correct
def validate_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = User.query.filter_by(user_id=data['userid']).first()
        return current_user
    except:
        return None


@app.route('/login', methods=["POST"])
def login():
    data = request.form.to_dict()
    username = data['username']
    password = data['password']
    if not username or not password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=username).first()
    print("\n",user.password," - ",user.username)
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, password):
        token = jwt.encode({'userid' : user.user_id}, app.config['SECRET_KEY'])
        response = make_response(redirect("/"))
        response.set_cookie('token', token)
        return response
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/', methods=['GET'])
def main_page():
    token = request.cookies.get('token')
    if token is None:
        return make_response(redirect('/login'))
    elif validate_token(token) is None:
        return jsonify({'message': 'Token is invalid!'}), 401
    else:
        return render_template("MainPage.html")


@app.route('/userinfo', methods=['GET'])
@token_required
def get_userinfo(current_user):
    return user_schema.jsonify(current_user)


# endpoint to user registeration
@app.route("/register", methods=["GET"])
def getRegisterPage():
    return render_template("Register.html");


# endpoint to user login
@app.route("/login", methods=["GET"])
def getLoginPage():
    return render_template("Login.html");


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    data= request.form.to_dict()
    username= data['username']
    email = data['email']
    password = data['password']
    hashed_password=generate_password_hash(password, method='sha256')
    new_user = User(username, email, hashed_password)


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
@token_required
def add_photo(currentuser):
    photo_path = request.json['photo_path']
    uploaded_by = currentuser.user_id

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


# endpoint to get photo detail by id
@app.route("/photo/<id>", methods=["GET"])
def photo_detail(id):
    photo = Photo.query.get(id)
    return photo_schema.jsonify(photo)


# endpoint to update photo
@app.route("/photo/<id>", methods=["PUT"])
def photo_update(id):
    tags = request.json['tags']

    # check if tag is already exists for that photo
    for tag in tags:
        # get all the photos with the tag
        res = Photo.query.filter(Photo.tags.any(Tag.tag_desc == tag)).all()
        # if there is no photo with the tag, add new tag assc with photo
        if not res:
            tab_obj = Tag(id, tag)
            db.session.add(tab_obj)

        # if there are photos with the tag, check if photo <id> has that tag
        else:
            for photo in res:
                if photo.photo_id != int(id):
                    tab_obj = Tag(id, tag)
                    db.session.add(tab_obj)

    db.session.commit()

    photo = Photo.query.get(id)
    return photo_schema.jsonify(photo)


# endpoint to delete photo
@app.route("/photo/<id>", methods=["DELETE"])
def photo_delete(id):
    photo = Photo.query.get(id)
    db.session.delete(photo)
    db.session.commit()

    return photo_schema.jsonify(photo)


# endpoint to search tags
@app.route("/tag/<tag>", methods=["GET"])
def search_tag(tag):
    photos_with_tag = Photo.query.filter(Photo.tags.any(Tag.tag_desc == tag))

    return photos_schema.jsonify(photos_with_tag)


### ALBUM
# endpoint to create new album
@app.route("/album", methods=["POST"])
@token_required
def add_album(currentuser):
    album_name = request.json['album_name']
    owner = currentuser.user_id
    new_album = Album(album_name, owner)

    db.session.add(new_album)
    db.session.commit()

    return album_schema.jsonify(new_album)


# endpoint to show all albums
@app.route("/album", methods=["GET"])
def get_album():
    all_albums = Album.query.all()
    result = albums_schema.dump(all_albums)
    return albums_schema.jsonify(result.data)


# endpoint to get album detail by id
@app.route("/album/<id>", methods=["GET"])
def album_detail(id):
    album = Album.query.get(id)
    return album_schema.jsonify(album)


# endpoint to update album
@app.route("/album/<id>", methods=["PUT"])
def album_update(id):
    album = Album.query.get(id)
    album_name = request.json['album_name']

    album.album_name = album_name

    db.session.commit()
    return album_schema.jsonify(album)


# endpoint to delete album
@app.route("/album/<id>", methods=["DELETE"])
def album_delete(id):
    album = Album.query.get(id)
    db.session.delete(album)
    db.session.commit()

    return album_schema.jsonify(album)


if __name__ == '__main__':
    app.run(debug=True)
