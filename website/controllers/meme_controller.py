from sqlalchemy import desc
from flask import Blueprint, render_template, request, redirect, flash, abort, jsonify
from flask_login import login_required, current_user
from flask.helpers import url_for
from ..database.meme_model import Meme
from ..database.tag_model import Tag
from ..database import db
from ..models.meme_model import MemeType, convert_to_memetype
import os
import json

meme_blueprint = Blueprint('meme',__name__)

@meme_blueprint.route('/getpage')
def get_page():
    num = int(request.args.get('num',0))
    if num == 0:
        abort(404)
    tags = request.args.get('search', None)
    memes = Meme.query.order_by(desc(Meme.date)).paginate(page=int(num),per_page=50,error_out=False).items
    if search != None:
        memes = search(tags,num)
    if len(memes) == 0:
        return ''
    memesT = convert_to_memetype(memes)
    return json.dumps([MemeType.toJSON(self=meme) for meme in memesT])

@meme_blueprint.route('/upload')
@login_required
def upload():
    '''Displays the upload page.'''
    return render_template('meme/upload.html')

@meme_blueprint.route('/upload',methods=['POST'])
@login_required
def upload_file():
    '''Uploads the image into its required folder and adds the url 
    for the image to the database and redirects back to homepage.'''
    file = request.files['file']
    tagtext = request.form.get('tags')
    if file.filename == '' or tagtext == '':
        flash('Didn\'t submit required infromation!', category='error')
        return redirect(url_for('public.home'))
    extention = os.path.splitext(file.filename)[1]
    memes = Meme.query.all()
    id = 0
    if len(memes) == 0:
        id = 1
    else:
        id = memes[-1].id+1
    if os.getcwd() != 'Z:\memebank\website\\templates':
        os.chdir('website/templates')
    path = '../static/memes/meme'+str(id)+extention
    file.save(path)
    tags = tagtext.split()
    saved_tags = []
    for tag in tags:
        dbTag = db.session.query(Tag).filter(Tag.name==tag).scalar()
        if not dbTag:
            dbTag = Tag(name=tag)
        saved_tags.append(dbTag)

    meme = Meme(url=path,tags=saved_tags, user_id=current_user.id)
    db.session.add(meme)
    db.session.commit()
    flash('Meme Succefully Uploaded!', category='success')
    return redirect(url_for('public.home'))

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
    It combines each list of memes into one list and runs combine_memes and then 
    convert_to_memetype on the combined list and displays and passes the memes 
    to the search page.'''
    tags = request.args.get('search')
    if not tags or tags == '':
        flash('Invaild Search!', category='error')
        return redirect(url_for('public.home'))
    combined_memes = search(tags,1)
    memesT = convert_to_memetype(combined_memes)
    result = {'search': tags, 'memes': memesT}
    return render_template('meme/search.html', res=result)

def search(tags, page_num):
    multi_memes = []
    for tag in tags.split():
        dbTag = db.session.query(Tag).filter(Tag.name == tag).scalar()
        if dbTag:
            multi_memes.append(dbTag.memes)
    return combine_memes(multi_memes)   

def combine_memes(memeslist):
    '''Takes a list of sublists of memes from the database and combines
    them into one list retaining the order of the sublists.'''
    maxlength = 0
    for memes in memeslist:
        if len(memes) > maxlength:
            maxlength = len(memes)
    results = []
    for i in range(maxlength):
        for memes in memeslist:
            if i < len(memes):
                results.append(memes[i])
    return sort_combined_memes(results)

def sort_combined_memes(memes):
    if len(memes) < 2:
        return memes
    smaller = []
    larger = []
    equal = []
    for meme in memes:
        if memes[0].date > meme.date:
            smaller.append(meme)
        elif memes[0].date < meme.date:
            larger.append(meme)
        elif memes[0].date == meme.date:
            equal.append(meme)
    return sort_combined_memes(larger) + equal + sort_combined_memes(smaller)
