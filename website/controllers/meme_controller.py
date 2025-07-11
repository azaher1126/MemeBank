from sqlalchemy import desc, and_
from flask import Blueprint, render_template, request, redirect, flash, abort, jsonify, send_from_directory
from flask_login import login_required, current_user
from flask.helpers import url_for
from ..database.meme_model import Meme
from ..database.tag_model import Tag
from ..database import db
from ..models.meme_model import MemeType, convert_to_memetype
from ..forms.meme_upload_form import MemeUploadForm
from ..forms import flash_errors
from ..uploads.meme_uploads import meme_uploads
import os

meme_blueprint = Blueprint('meme',__name__)

@meme_blueprint.route('/upload',methods=['GET','POST'])
@login_required
def upload_file():
    '''Uploads the image into its required folder and adds the url 
    for the image to the database and redirects back to homepage.'''
    upload_form: MemeUploadForm = MemeUploadForm()
    if upload_form.validate_on_submit():
        meme_rec = Meme(user_id=current_user.id)
        db.session.add(meme_rec)

        tags = upload_form.get_tags()
        for tag in tags:
            dbTag = db.session.query(Tag).filter(Tag.name==tag).scalar()
            if not dbTag:
                dbTag = Tag(name=tag)
            meme_rec.tags.append(dbTag)

        file = upload_form.meme.data
        extension = os.path.splitext(file.filename)[1]

        filename = f'meme_{meme_rec.id}{extension}'
        meme_uploads.save(file, name=filename)
        meme_rec.url = filename

        db.session.commit()
        flash('Meme Successfully Uploaded!', category='success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(upload_form)
    return render_template('meme/upload.html', upload_form=upload_form)

@meme_blueprint.route('/meme/image/<path:id>')
def get_meme_image(id):
    meme_rec = db.session.query(Meme).filter(Meme.id == id).first()
    if not meme_rec:
        abort(404)
    return send_from_directory(meme_uploads.config.destination, meme_rec.url)

@meme_blueprint.route('/meme/<path:id>')
def view_meme(id):
    '''Gets the meme by its id then displays the meme page and 
    passes the meme data to the page'''
    meme = Meme.query.filter_by(id=id).first()
    memeT = MemeType(meme)
    return render_template('meme/meme.html',meme=memeT)

@meme_blueprint.route('/api/like', methods=['POST'])
def like():
    if not current_user.is_authenticated:
        flash('Please log in to start liking memes!', 'error')
        abort(401)
    meme_id = request.form.get('id')
    if not meme_id:
        flash('There was an error while processing your request, please try again.', 'error')
        abort(400)
    meme = Meme.query.filter_by(id=meme_id).first()
    if not meme:
        flash('Unable to locate meme, it may have been deleted.', 'error')
        abort(404)
    if current_user not in meme.users_liked:
        meme.users_liked.append(current_user)
        db.session.commit()
    return jsonify(MemeType(meme))

@meme_blueprint.route('/api/unlike', methods=['POST'])
def unlike():
    if not current_user.is_authenticated:
        flash('Please log in to start unliking memes!', 'error')
        abort(401)
    meme_id = request.form.get('id')
    if not meme_id:
        flash('There was an error while processing your request, please try again.', 'error')
        abort(400)
    meme = Meme.query.filter_by(id=meme_id).first()
    if not meme:
        flash('Unable to locate meme, it may have been deleted.', 'error')
        abort(404)
    if current_user in meme.users_liked:
        meme.users_liked.remove(current_user)
        db.session.commit()
    return jsonify(MemeType(meme))

@meme_blueprint.route('/search', methods=['GET'])
def search():
    '''Gets the string that the user would like to search with then 
    splits it into individual tags and searches the database for each tag.
    It combines all of the memes into a single list and sorts it from newest
    to oldest and passes the first 20 memes to the search page.'''
    tags = request.args.get('search')
    if not tags or tags == '':
        flash('Invaild Search!', category='error')
        return redirect(url_for('public.home'))
    last_id = request.args.get('last_id')
    
    combined_memes = search(tags, last_id)
    memesT = convert_to_memetype(combined_memes)
    if not last_id:
        result = {'search': tags, 'memes': memesT}
        return render_template('meme/search.html', res=result)
    return render_template('components/meme_page.html', memes=memesT)

def search(tags: str, last_id: int | None):
    multi_memes = []
    split_tags = [tag.strip() for tag in tags.split(',')]
    db_tags = db.session.query(Tag).filter(Tag.name.in_(split_tags)).all()
    if len(db_tags) == 0:
        return multi_memes
    
    tag_ids = [db_tag.id for db_tag in db_tags]
    if not last_id:
        db_memes = db.session.query(Meme).filter(Meme.tags.any(Tag.id.in_(tag_ids))).order_by(desc(Meme.date)).limit(20).all()
        return db_memes
    db_memes = db.session.query(Meme).filter(and_(Meme.id < last_id, Meme.tags.any(Tag.id.in_(tag_ids)))).order_by(desc(Meme.date)).limit(20).all()
    return db_memes