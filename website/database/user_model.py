from . import db
from .liked_entry import like_entries
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    profile_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    memes = db.relationship('Meme', back_populates='uploader', cascade="all, delete-orphan")
    default_sorting = db.Column(db.Integer)

    liked_memes = db.relationship('Meme', secondary=like_entries, back_populates='users_liked')