# Import flask dependencies
from flask import Blueprint, render_template

# Import needed models
from putbox.auth.AuthService import Auth
from putbox.photos.models import Photo, Tag

# Define the blueprint: 'tag'
mod_tag = Blueprint('tag', __name__, url_prefix='/tag')


# endpoint to search tags
@mod_tag.route("/<tag>", methods=["GET"])
@Auth.token_required
def search_tag(current_user, tag):
    photos_with_tag = Photo.query\
                .filter(Photo.tags.any(Tag.tag_desc == tag)) \
                .filter(Photo.uploaded_by == current_user.user_id)

    # result = photos_schema.dumps(photos_with_tag)
    # res = json.loads(result.data)
    return render_template("Search.html", photos=photos_with_tag)