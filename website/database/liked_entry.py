from . import db
from sqlalchemy.sql import func

like_entries = db.Table('LikedEntries', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('meme_id', db.Integer, db.ForeignKey('Memes.id'), primary_key=True),
    db.Column('liked_at', db.DateTime(timezone=True), default=func.now()))
