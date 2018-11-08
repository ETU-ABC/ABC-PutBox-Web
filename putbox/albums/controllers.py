# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  jsonify, g, session, redirect, make_response

# Import the database object from the main app module
from putbox import db

# Import module models
from putbox.auth.AuthService import Auth
from putbox.albums.models import Album
from putbox.albums.schemas import album_schema, albums_schema

# Import json
import json

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_album = Blueprint('album', __name__, url_prefix='/album')


# endpoint to show all albums
@mod_album.route("/", methods=['GET'])
@Auth.token_required
def get_all_photos(current_user):
    all_albums = Album.query.filter(Album.owner == current_user.user_id)
    result = albums_schema.dumps(all_albums)
    res = json.loads(result.data)
    return render_template("MainPage.html", albums=res, owner=1)


# endpoint to create new album
@mod_album.route("/", methods=["POST"], strict_slashes=False)
@Auth.token_required
def add_album(current_user):
    album_name = request.json['album_name']
    owner = current_user.user_id
    new_album = Album(album_name, owner)

    db.session.add(new_album)
    db.session.commit()

    return album_schema.jsonify(new_album)


# endpoint to show all the photos in an album
@mod_album.route("/<id>", methods=['GET'])
@Auth.token_required
def get_album(current_user, id):
    # TODO
    # photos = Photo.query\
    #         .filter(Photo.uploaded_by == current_user.user_id)\
    #         .filter(Photo.album_id == id)
    # result = photos_schema.dumps(photos)
    # res = json.loads(result.data)
    return render_template("AlbumPage.html", album_id=id,photos=res, owner_album=current_user.username)


# endpoint to update album
@mod_album.route("/<id>", methods=["PUT"])
@Auth.token_required
def album_update(id):
    album = Album.query.get(id)
    album_name = request.json['album_name']

    album.album_name = album_name

    db.session.commit()
    return album_schema.jsonify(album)


# endpoint to delete album
@mod_album.route("/<id>", methods=["DELETE"])
@Auth.token_required
def album_delete(id):
    album = Album.query.get(id)
    db.session.delete(album)
    db.session.commit()

    return album_schema.jsonify(album)


