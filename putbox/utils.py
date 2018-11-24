# Import os for random number generate
import uuid


def random_hash():
    return uuid.uuid4().hex[:8]
