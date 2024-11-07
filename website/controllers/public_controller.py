from sqlalchemy import desc
from flask import Blueprint, render_template, request, abort
from ..database import db
from ..database.meme_model import Meme
from ..models.meme_model import convert_to_memetype

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route('/')
def home():
    '''Displays and passes all memes to the home page.'''
    last_id = request.args.get('last_id')
    if not last_id:
        memes = db.session.query(Meme).order_by(desc(Meme.date)).limit(20).all()
        memesT = convert_to_memetype(memes)
        return render_template('public/home.html', memes=memesT)
    # Page is requesting more memes
    last_meme = db.session.query(Meme).filter(Meme.id == last_id).first()
    if not last_meme:
        abort(404)
    memes = db.session.query(Meme).order_by(desc(Meme.date)).filter(Meme.id < last_meme.id).limit(20).all()
    memesT = convert_to_memetype(memes)
    return render_template('components/meme_page.html', memes=memesT)

@public_blueprint.route('/about')
def about():
    '''Displays the credits page'''
    return render_template('public/about.html')
