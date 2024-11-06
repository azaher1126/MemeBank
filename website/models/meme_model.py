from . import db
from sqlalchemy.sql import func

class Meme(db.Model):
    __tablename__ = 'Memes'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    tags = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    liked = db.Column(db.String(10000), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    username = db.Column(db.String(150))