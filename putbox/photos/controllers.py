# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  jsonify, g, session, redirect, make_response

#import datetime (i.e. current time)
import datetime

# Import the database object & photo_upload from the main app module
from putbox import db, photo_upload

# Import module models
from putbox.auth.AuthService import Auth
# Import module models (i.e. User)
from putbox.auth.models import Users
# Import module models (i.e. Photo)
from putbox.photos.models import Photo, SharedPhoto
# Import module models (i.e. Like)
from putbox.photos.models import Like
#Import thread for scheduling
import threading
import time

# App utils
import putbox.utils


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_photo = Blueprint('photo', __name__, url_prefix='/photo')


def delete_time_photo(id,time_input):
    time.sleep(time_input)
    photo = Photo.query.get(id)
    db.session.delete(photo)
    db.session.commit()
    return None

# endpoint to insert new photo
@mod_photo.route("/", methods=["POST"], strict_slashes=False)
@Auth.token_required
def add_photo(current_user):
    if 'photo' in request.files:
        filename = photo_upload.save(request.files['photo'])
        photo_path = 'photos/' + filename
    else:
        return "No image found!", 415
    data = request.form.to_dict()
    album_id = data['album_id']
    uploaded_by = current_user.user_id
    new_photo = Photo(photo_path, uploaded_by, album_id)
    db.session.add(new_photo)
    db.session.commit()

    #Set_Photo_delete_time
    user = Users.query.filter_by(user_id=current_user.user_id).first()
    photo_id= str(new_photo.photo_id)
    time_input = 60*(user.auto_delete_time)
    #Set thread
    thread = threading.Thread(target=delete_time_photo, args=[photo_id,time_input])
    thread.start()

    return redirect("/album/"+album_id, code=302)


# endpoint to show all photos of the user
@mod_photo.route("/", methods=["GET"])
def get_photo():
    """""
    all_photos = Photo.query.all()
    result = photos_schema.dump(all_photos)
    return photos_schema.jsonify(result.data)
    """
    return render_template("PhotoPage.html", photos=[

    ], owner_album = 1)


# endpoint to get photo detail by id
# if request made by the photo_owner
@mod_photo.route("/<id>", methods=["GET"])
@Auth.token_required
def photo_detail(current_user, id):
    share_key = request.args.get('shared')
    # if this is not for viewing a shared photo
    # show the user himself/herself photo
    if share_key is None:
        photo = Photo.query.get(id)
        if photo is None:
            return redirect("/", code=302)
        elif photo.uploaded_by == current_user.user_id:
            return render_template("PhotoPage.html", photo=photo)
        else:
            return redirect("/", code=302)
            #return make_response(jsonify({"error": "You have not permission to view the photo!"}), 401)
    else:
        # show the shared photo
        shared_photo_entry = SharedPhoto.query.filter_by(share_key=share_key). \
            filter_by(photo_id=id).first()
        if shared_photo_entry is None:
            return "Wrong share key!"
        else:
            shared_photo = Photo.query.get(shared_photo_entry.photo_id)
            return render_template("PhotoPage.html", photo=shared_photo)


# endpoint to delete photo
@mod_photo.route("/<id>", methods=["DELETE"])
@Auth.token_required
def photo_delete(current_user, id):
    photo = Photo.query.get(id)

    # TODO handle the code duplication for checking photo owner
    if photo.uploaded_by == current_user.user_id:
        db.session.delete(photo)
        db.session.commit()
        # return photo_schema.jsonify(photo)
        return None
    else:
        return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)


@mod_photo.route("/like/<id>",methods=["POST"])
@Auth.token_required
def add_photo_like(current_user, id):
    photo = Photo.query.get(id)

    if photo.uploaded_by == current_user.user_id:
        like_obj = Like(id, current_user.user_id)
        db.session.add(like_obj)
        db.session.commit()
        return None
    else:
        return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)



@mod_photo.route("/like/<id>",methods=["GET"])
@Auth.token_required
def get_photo_like(current_user, id):
    photo = Photo.query.get(id)

    # TODO handle the code duplication for checking photo owner
    if photo.uploaded_by == current_user.user_id:
        liked_by = Like.query.filter_by(photo_id=id)
        return None


@mod_photo.route('/<id>/share', methods=['GET'])
@Auth.token_required
def share_the_photo(current_user, id):
    # get photo
    photo = Photo.query.get(id)

    if photo is None:
        return "Photo not found with given id!"
    elif photo.uploaded_by != current_user.user_id:
        return "You can only share your own photos!"
    else:
        share_key = putbox.utils.random_hash()
        shared_photo = SharedPhoto(id, share_key)
        db.session.add(shared_photo)
        db.session.commit()

        # Build the share url
        base_url = request.url_root  # http://localhost:5000/
        share_url = base_url + 'photo/' + id + '?shared=' + share_key
        return share_url

