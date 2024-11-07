from functools import wraps

from flask import flash, redirect
from flask_login import current_user


def anonymous_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            flash('The requested page is only accessible to logged out users.', 'error')
            return redirect('/')  # Forbidden
        return func(*args, **kwargs)

    return wrapper
