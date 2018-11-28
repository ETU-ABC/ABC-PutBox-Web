# Import os for random number generate
import uuid
from config import cred


def random_hash():
    return uuid.uuid4().hex[:8]


# Firebase access token
def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """

    access_token_info = cred.get_access_token()
    return access_token_info.access_token
