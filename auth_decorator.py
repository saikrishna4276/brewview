

from flask import *
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('user', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return 'You aint logged in, no page for u!'
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if session['user'] != 'admin':
            abort(403)
              # Forbidden access
        return func(*args, **kwargs)
    return decorated_view