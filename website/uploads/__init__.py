from flask import Flask
from flask_uploads import configure_uploads
from os import path, mkdir

def initialize_uploads(app: Flask):
    uploads_directory = path.dirname(__file__)

    app.config['UPLOADS_DEFAULT_DEST'] = uploads_directory
    
    from .meme_uploads import meme_uploads
    configure_uploads(app, (meme_uploads))
