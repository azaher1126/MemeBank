from flask import Flask
from flask_uploads import configure_uploads
from os import path, mkdir

def initialize_uploads(app: Flask):
    base_path = app.config.get('UPLOADS_BASE_PATH')
    if base_path:
        app.config['UPLOADS_DEFAULT_DEST'] = base_path
    else:
        uploads_directory = path.dirname(__file__)
        app.config['UPLOADS_DEFAULT_DEST'] = uploads_directory
    
    from .meme_uploads import meme_uploads
    configure_uploads(app, (meme_uploads))
