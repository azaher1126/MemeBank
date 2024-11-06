from flask import Flask
from .meme_controller import meme_blueprint
from .public_controller import public_blueprint
from .account_controller import account_blueprint

def intialize_controllers(app: Flask):    
    app.register_blueprint(public_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(meme_blueprint)