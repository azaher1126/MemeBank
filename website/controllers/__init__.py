from flask import Flask
from .meme_controller import meme_blueprint
from .public_controller import public_blueprint
from .account_controller import account_blueprint
from .settings_controller import settings_blueprint

def initialize_controllers(app: Flask):    
    app.register_blueprint(public_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(meme_blueprint)
    app.register_blueprint(settings_blueprint)