from flask import current_app, request
from flask_login import login_required as login_required_org
from urllib.parse import urlparse

LOGIN_REQUIRED = "__login_required__"

def login_required(func):
    wrapped = login_required_org(func)
    setattr(wrapped, LOGIN_REQUIRED, True)
    return wrapped

def is_login_required(url: str):
    parsed_url = urlparse(url)
    try:
        endpoint, _ = current_app.url_map.bind_to_environ(request.environ).match(parsed_url.path)
        view_func = current_app.view_functions.get(endpoint)
        if not view_func:
            return False
        
        return hasattr(view_func, LOGIN_REQUIRED)
    except Exception:
        raise ValueError("The URL provided is not served by this application.")
