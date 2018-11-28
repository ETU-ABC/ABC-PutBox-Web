# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  jsonify, g, session, redirect, make_response
import json
from putbox import db, photo_upload
from putbox.auth.AuthService import Auth
from putbox.auth.models import Users
from putbox.photos.models import Photo, SharedPhoto
from putbox.photos.models import Like
import threading
import time
import putbox.utils

#import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
cred = credentials.Certificate("./putbox/photos/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

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
            user = Users.query.filter_by(user_id=current_user.user_id).first()
            photo = Photo.query.get(id)
            uploaded_by = photo.uploaded_by
            return render_template("PhotoPage.html", photo=shared_photo,current_user=user.username,photo_owner=uploaded_by)


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
def add_photo_like(current_user,id):

    photo = Photo.query.get(id)
    photo_owner = Users.query.filter_by(user_id=photo.uploaded_by).first()
    if photo.uploaded_by == current_user.user_id:
        like_obj = Like(id, current_user.username)
        db.session.add(like_obj)
        db.session.commit()
        url = "https://fcm.googleapis.com/fcm/send"
        topic = photo_owner.user_token

        # See documentation on defining a message payload.
        message = messaging.Message(
            data={
                "body": "Bu bildirime tıklayarak fotoğrafınıza erişebilirsiniz!",
                "title": "{} kişisi fotoğrafınızı beğendi".format(current_user.username),
                "url": "http://putbox-abc.herokuapp.com/photo/{}".format(id)
            },
            topic=topic,
        )


        response = messaging.send(message)

        print('Successfully sent message:', response)
        message = {"sender_user" : current_user.username, "photo_owner":photo_owner.username, "photo_id": id }
        return make_response(json.dumps(message), 200)

    else:
        return make_response(jsonify({"error":"You have not permission to view the photo!"}), 401)

def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """

  access_token_info = cred.get_access_token()
  return access_token_info.access_token

@mod_photo.route("/like/<id>",methods=["GET"])
@Auth.token_required
def get_photo_like(current_user, id):
    photo = Photo.query.get(id)

    # TODO handle the code duplication for checking photo owner
    if photo.uploaded_by == current_user.user_id:
        liked_by = Like.query.filter_by(photo_id=id)
        #return
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
        return redirect(share_url)
