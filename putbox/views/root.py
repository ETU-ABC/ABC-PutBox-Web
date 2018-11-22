# Import flask dependencies
from flask import Blueprint, request, render_template

# Import album
from putbox.albums import controllers
# Define the blueprint: 'root'
mod_root = Blueprint('root', __name__)


@mod_root.route('/', methods=['GET'])
def index():
    token = request.cookies.get('token')
    if token is None:
        # user not logged in
        return render_template('Login.html')
    else:
        # return redirect('/album')
        return controllers.get_all_photos()
