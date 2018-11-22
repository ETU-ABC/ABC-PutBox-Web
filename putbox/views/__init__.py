# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module
from putbox.auth.controllers import mod_auth as auth_module
from putbox.photos.controllers import mod_photo as photo_module
from putbox.albums.controllers import mod_album as album_module
from putbox.auth.controllers import mod_user as user_module
from .root import mod_root as root_module
