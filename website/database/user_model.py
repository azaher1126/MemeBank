from . import db
from .helpers.custom_types import TimeStamp
from .liked_entry import like_entries
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    profile_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    username_colour = db.Column(db.String(7), nullable=False, default='#ffffff', server_default='#ffffff')
    memes = db.relationship('Meme', back_populates='uploader', cascade="all, delete-orphan")
    default_sorting = db.Column(db.Integer)
    created_at = db.Column(TimeStamp(timezone=True), default=func.now(), nullable=False)

    liked_memes = db.relationship('Meme', secondary=like_entries, back_populates='users_liked')