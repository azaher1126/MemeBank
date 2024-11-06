from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, stamp, upgrade
from os import path

db = SQLAlchemy()
migrate = Migrate()

def initialize_database(app, db_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from . import user_model, meme_model
    db.init_app(app)

    db_directory = path.dirname(__file__)

    migrations_directory = path.join(db_directory, 'migrations')
    migrate.init_app(app, db, directory=migrations_directory)

    with app.app_context():
        '''Initilizes the databse file and sets up the table.'''
        if not path.exists(db_path):
            db.create_all()
            stamp()
            print('Created!')
        else:
            upgrade()
