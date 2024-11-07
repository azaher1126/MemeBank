from . import db
from .tag_entry import tag_entries
from sqlalchemy.sql import func

class Tag(db.Model):
    __tablename__ = 'Tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    memes = db.relationship('Meme', secondary=tag_entries, back_populates='tags')