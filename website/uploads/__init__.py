from flask import Flask
from os import path

from .helpers.image_upload_set import configure_uploads

def initialize_uploads(app: Flask):
    base_path = app.config.get('UPLOADS_BASE_PATH')
    if not base_path:
        base_path = path.dirname(__file__)

    configure_uploads(base_path)
