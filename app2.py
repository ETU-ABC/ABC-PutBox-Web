from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
import os
import datetime
import jwt
import json
from functools import wraps
#from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from flask_heroku import Heroku

# the values of those depend on your setup
POSTGRES_URL = "ec2-54-228-181-43.eu-west-1.compute.amazonaws.com:5432"
POSTGRES_USER = "bhywntahknhkfs"
POSTGRES_PW = "4c47fe4a36b1fcd559b17aa5fd88618d9dd7765467de6c78ec9e5ff8599ccf81"
POSTGRES_DB = "d277ase0i9t3ct"

#app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bil495-abc.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
#app.config['SECRET_KEY'] = 'etu-abc-putbox'

# IMAGE UPLOAD
#PHOTOS = UploadSet('photos', IMAGES)

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/photos'
#configure_uploads(app, PHOTOS)

heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)



# class Photo(db.Model):
#     photo_id = db.Column(db.Integer, primary_key=True)
#     photo_path = db.Column(db.String, unique=True)
#     upload_date = db.Column(db.DateTime)
#     uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     tags = relationship("Tag")
#     album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
#
#     def __init__(self, photo_path, uploaded_by, album_id):
#         self.photo_path = photo_path
#         self.uploaded_by = uploaded_by
#         self.upload_date = datetime.datetime.now()
#         self.album_id = album_id
#
#
# class PhotoSchema(ma.Schema):
#     class Meta:
#         fields = ('photo_id', 'album_id', 'photo_path', 'upload_date', 'uploaded_by', 'tags')
#     tags = ma.Nested('TagSchema', many=True, only=['tag_desc'])
#
#
# photo_schema = PhotoSchema()
# photos_schema = PhotoSchema(many=True)


# class Tag(db.Model):
#     tag_id = db.Column(db.Integer, primary_key=True)
#     photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'))
#     tag_desc = db.Column(db.String)
#
#     def __init__(self, photo_id, tag_desc):
#         self.photo_id = photo_id
#         self.tag_desc = tag_desc
#
#
# class TagSchema(ma.Schema):
#     class Meta:
#         fields = ('photo_id', 'tag_desc')
#
#
# tag_schema = TagSchema()
# tags_schema = TagSchema(many=True)


# class Album(db.Model):
#     album_id = db.Column(db.Integer, primary_key=True)
#     album_name = db.Column(db.String, unique=True)
#     owner = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     # TODO album cover is set to first photo in the album
#     # cover = db.Column(Integer, ForeignKey('photo.photo_id'))
#     photos = relationship("Photo")
#
#     def __init__(self, album_name, owner):
#         self.album_name = album_name
#         self.owner = owner
#
#
# class AlbumSchema(ma.Schema):
#     class Meta:
#         fields = ('album_name', 'album_id', 'owner', 'photos')
#     photos = ma.Nested('PhotoSchema', many=True, exclude=('album_id',))
#
#
# album_schema = AlbumSchema()
# albums_schema = AlbumSchema(many=True)


#------AUTH------
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#
#         if 'token' in request.cookies:
#             token = request.cookies.get('token')
#
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401
#
#         current_user = validate_token(token)
#         if current_user is None:
#             return jsonify({'message': 'Token is invalid!'}), 401
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated


# # validate if token is signatured and correct
# def validate_token(token):
#     try:
#         data = jwt.decode(token, app.config['SECRET_KEY'])
#         current_user = Users.query.filter_by(user_id=data['userid']).first()
#         return current_user
#     except:
#         return None


# @app.route('/login', methods=["POST"])
# def login():
#     data = request.json
#     username = data['username']
#     password = data['password']
#     if not username or not password:
#         return make_response('Could not verify', 401)
#
#     user = Users.query.filter_by(username=username).first()
#     #print("\n",user.password," - ",user.username)
#     if not user:
#         return make_response('Could not verify', 401)
#     if check_password_hash(user.password, password):
#         token = jwt.encode({'userid' : user.user_id}, app.config['SECRET_KEY'])
#         out = jsonify(success=True)
#         out.set_cookie('token', token)
#         return out
#     return make_response('Could not verify', 401)


@app.route('/', methods=['GET'])
def main_page():
    token = request.cookies.get('token')
    if token is None:
        return make_response(redirect('/login'))
    elif validate_token(token) is None:
        return jsonify({'message': 'Token is invalid!'}), 401
    else:
        return getMainPage()



# endpoint to user registeration
@app.route("/register", methods=["GET"])
def getRegisterPage():
    return render_template("Register.html");


# endpoint to user login
@app.route("/login", methods=["GET"])
def getLoginPage():
    return render_template("Login.html");


# # endpoint to create new user
# @app.route("/users/signup", methods=["POST"])
# def add_user():
#     data=request.json
#     username=data['username']
#     email = data['email']
#     password = data['password']
#     hashed_password=generate_password_hash(password, method='sha256')
#     new_user = Users(username, email, hashed_password)
#
#     db.session.add(new_user)
#     db.session.commit()
#     return user_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# # endpoint to insert new photo
# @app.route("/photo", methods=["POST"])
# @token_required
# def add_photo(current_user):
#     if 'photo' in request.files:
#         filename = PHOTOS.save(request.files['photo'])
#         photo_path = PHOTOS.path(filename)
#     else:
#         return "No image found!", 415
#     data = request.form.to_dict()
#     album_id = data['album_id']
#     uploaded_by = current_user.user_id
#     photo_path = "../../" + photo_path
#     new_photo = Photo(photo_path, uploaded_by, album_id)
#
#     db.session.add(new_photo)
#     db.session.commit()
#
#     return redirect("/album/"+album_id, code=302)
#
#
# # endpoint to show all photos of the user
# @app.route("/photo", methods=["GET"])
# def get_photo():
#     """""
#     all_photos = Photo.query.all()
#     result = photos_schema.dump(all_photos)
#     return photos_schema.jsonify(result.data)
#     """
#     return render_template("PhotoPage.html", photos=[
#
#     ], owner_album = 1)
#
#
# # endpoint to get photo detail by id
# # if request made by the photo_owner
# @app.route("/photo/<id>", methods=["GET"])
# @token_required
# def photo_detail(current_user, id):
#
#     photo = Photo.query.get(id)
#     #print(current_user.user_id)
#     #print(photo.tags)
#     if photo is None:
#         return redirect("/", code=302)
#     elif photo.uploaded_by == current_user.user_id:
#         return render_template("PhotoPage.html", photo=photo)
#     else:
#         return redirect("/", code=302)
#         #return make_response(jsonify({"error": "You have not permission to view the photo!"}), 401)
#
#
# # endpoint to delete photo
# @app.route("/photo/<id>", methods=["DELETE"])
# @token_required
# def photo_delete(current_user, id):
#     photo = Photo.query.get(id)
#
#     # TODO handle the code duplication for checking photo owner
#     if photo.uploaded_by == current_user.user_id:
#         db.session.delete(photo)
#         db.session.commit()
#         return photo_schema.jsonify(photo)
#     else:
#         return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)


# TAG-RELATED ENDPOINTS

# endpoint to search tags
@app.route("/tag/<tag>", methods=["GET"])
@token_required
def search_tag(current_user, tag):
    photos_with_tag = Photo.query\
                .filter(Photo.tags.any(Tag.tag_desc == tag)) \
                .filter(Photo.uploaded_by == current_user.user_id)

    result = photos_schema.dumps(photos_with_tag)
    res = json.loads(result.data)
    return render_template("Search.html", photos=res)


# endpoint to add a tag to the photo
@app.route("/photo/<id>/tag", methods=["POST"])
@token_required
def tag_add(current_user, id):
    new_tag = request.json['tag']

    photo = Photo.query.get(id)
    if photo.uploaded_by == current_user.user_id:
        # check if tag already exists for that photo
        for tag in photo.tags:
            if tag.tag_desc == new_tag:
                return make_response(jsonify({"error": "Photo already has the tag!"}), 400)

        tag_obj = Tag(id, new_tag)
        db.session.add(tag_obj)
        db.session.commit()

        return photo_schema.jsonify(photo)
    else:
        return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)


# endpoint to delete a tag from the photo
@app.route("/photo/<id>/tag", methods=["DELETE"])
@token_required
def tag_delete(current_user, id):
    tag_to_delete = request.json['tag']

    photo = Photo.query.get(id)

    if photo.uploaded_by == current_user.user_id:
        # check if tag exists for that photo
        for tag in photo.tags:
            if tag.tag_desc == tag_to_delete:
                db.session.delete(tag)
                db.session.commit()
                return photo_schema.jsonify(photo)

        return make_response(jsonify({"error": "Photo does not have the tag!"}), 400)

    else:
        return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)


# #           ALBUM
# # endpoint to create new album
# @app.route("/album", methods=["POST"])
# @token_required
# def add_album(currentuser):
#     album_name = request.json['album_name']
#     owner = currentuser.user_id
#     new_album = Album(album_name, owner)
#
#     db.session.add(new_album)
#     db.session.commit()
#
#     return album_schema.jsonify(new_album)
#
#
# # endpoint to show all the photos in an album
# @app.route("/album/<id>", methods=['GET'])
# @token_required
# def get_album(current_user, id):
#     photos = Photo.query\
#             .filter(Photo.uploaded_by == current_user.user_id)\
#             .filter(Photo.album_id == id)
#     result = photos_schema.dumps(photos)
#     res = json.loads(result.data)
#     return render_template("AlbumPage.html", album_id=id,photos=res, owner_album=current_user.username)
#
#
# # endpoint to update album
# @app.route("/album/<id>", methods=["PUT"])
# def album_update(id):
#     album = Album.query.get(id)
#     album_name = request.json['album_name']
#
#     album.album_name = album_name
#
#     db.session.commit()
#     return album_schema.jsonify(album)
#
#
# # endpoint to delete album
# @app.route("/album/<id>", methods=["DELETE"])
# def album_delete(id):
#     album = Album.query.get(id)
#     db.session.delete(album)
#     db.session.commit()
#
#     return album_schema.jsonify(album)
#
#
# # endpoint to show all albums
# @app.route("/album", methods=['GET'])
# @token_required
# def getMainPage(current_user):
#     all_albums = Album.query.filter(Album.owner == current_user.user_id)
#     result = albums_schema.dumps(all_albums)
#     res = json.loads(result.data)
#     return render_template("MainPage.html", albums=res, owner=1)

# endpoint to show settings
@app.route("/settings", methods=['GET'])
def getSettingsPage():
    return render_template("Settings.html");


if __name__ == '__main__':
    app.run(debug=True)
