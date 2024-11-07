from sqlalchemy import desc
from flask import Blueprint, render_template
from ..database.meme_model import Meme
from ..models.meme_model import convert_to_memetype

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route('/')
def home():
    '''Displays and passes all memes to the home page.'''
    memes = Meme.query.order_by(desc(Meme.date)).paginate(page=1,per_page=50).items
    memesT = convert_to_memetype(memes)
    return render_template('public/home.html', memes=memesT)

@public_blueprint.route('/about')
def about():
    '''Displays the credits page'''
    return render_template('public/about.html')
