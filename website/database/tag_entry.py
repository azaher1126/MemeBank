from . import db
from .helpers.custom_types import TimeStamp
from sqlalchemy.sql import func

tag_entries = db.Table('TagEntries', db.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('Tags.id'), primary_key=True),
    db.Column('meme_id', db.Integer, db.ForeignKey('Memes.id'), primary_key=True),
    db.Column('tagged_at', TimeStamp(timezone=True), default=func.now(), nullable=False))
