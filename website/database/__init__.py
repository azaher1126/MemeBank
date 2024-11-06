from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def initialize_database(app, db_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from . import user_model, meme_model
    db.init_app(app)

    with app.app_context():
        '''Initilizes the databse file and sets up the table.'''
        if not path.exists(db_path):
            db.create_all()
            print('Created!')
