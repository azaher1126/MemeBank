from flask import Flask
from flask_login import LoginManager
from os import path

from .controllers import initialize_controllers
from .database import initialize_database
from .uploads import initialize_uploads
from .forms import initialize_forms

from .config import Config, DevelopmentConfig

def create_app(config: Config = None) -> Flask:
    '''Creates the server instance and sets up all views and databases.'''
    app = Flask(__name__)
    app.config.from_object(config or DevelopmentConfig())
    app.config['MAX_CONTENT_LENGTH'] = 25165824

    initialize_database(app, config.DB_PATH)

    initialize_controllers(app)

    login_manager = LoginManager()
    login_manager.login_view = 'account.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    from .database.user_model import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    assets_dir = path.join(path.dirname(path.realpath(__file__)), 'assets')
    app.config['ASSETS_DIR_PATH'] = assets_dir
    
    initialize_uploads(app)
    initialize_forms(app)

    return app
