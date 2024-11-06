from flask import Flask
from flask_login import LoginManager
from os import path

from .controllers import intialize_controllers
from .models import initialize_database

DB_PATH = path.join(path.dirname(path.realpath(__file__)), 'database.db')

def create_app():
    '''Creats the server instance and sets up all views and databses.'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'memebank'

    initialize_database(app, DB_PATH)

    intialize_controllers(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    from .models.user_model import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
