from flask import Flask
from flask_login import LoginManager
from os import path

from .controllers import intialize_controllers
from .database import initialize_database
from .uploads import initialize_uploads

DB_PATH = path.join(path.dirname(path.realpath(__file__)), 'database.db')

def create_app():
    '''Creats the server instance and sets up all views and databses.'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'memebank'
    app.config['MAX_CONTENT_LENGTH'] = 25165824

    initialize_database(app, DB_PATH)

    intialize_controllers(app)

    login_manager = LoginManager()
    login_manager.login_view = 'account.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    from .database.user_model import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    initialize_uploads(app)

    return app
