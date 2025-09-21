from . import db
from .helpers.custom_types import TimeStamp
from .liked_entry import like_entries
from .tag_entry import tag_entries
from sqlalchemy.sql import func

class Meme(db.Model):
    __tablename__ = 'Memes'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    date = db.Column(TimeStamp(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    tags = db.relationship('Tag', secondary=tag_entries, back_populates='memes')

    uploader = db.relationship('User', back_populates='memes', foreign_keys=[user_id])
    users_liked = db.relationship('User', secondary=like_entries, back_populates='liked_memes')