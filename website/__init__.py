from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    '''Creats the server instance and sets up all views and databses.'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'memebank'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Meme, User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    '''Initilizes the databse file and sets up the table.'''
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created!')