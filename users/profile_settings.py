from customcaps.utils import get_filename
import os
HOST_OF_SERVER = 'localhost:8000'

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


USERS_UPLOAD_DIR = 'user/photo'

def users_photo_upload_to(instance, filename):
    new_filename = get_filename(filename)
    return os.path.join(USERS_UPLOAD_DIR, new_filename)