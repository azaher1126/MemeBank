from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    tags = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    liked = db.Column(db.String(10000), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    memes = db.relationship('Meme')
    default_sorting = db.Column(db.Integer)
    