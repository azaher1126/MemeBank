from sqlalchemy import or_, desc
from flask import Blueprint, render_template, request, redirect, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import url_for
from .models import Meme, User
from . import db
import os
import json

views = Blueprint('views',__name__)

@views.route('/')
def home():
    '''Displays and passes all memes to the home page.'''
    memes = Meme.query.order_by(desc(Meme.date)).paginate(page=1,per_page=50).items
    memesT = convert_to_memetype(memes)
    return render_template('home.html', memes=memesT)

@views.route('/getpage')
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

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        profile_name = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists.', category='error')
        elif profile_name:
            flash('Username already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif '@queensu.ca' not in email:
            flash('Email must end with @queensu.ca', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rememeber_me = request.form.get('remember-me')
        user = User.query.filter(or_(User.email==email,User.username==email)).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=rememeber_me)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/forget_password')
def forget_password():
    return render_template('forget_password.html')

@views.route('/upload')
@login_required
def upload():
    '''Displays the upload page.'''
    return render_template('upload.html')

@views.route('/upload',methods=['POST'])
@login_required
def upload_file():
    '''Uploads the image into its required folder and adds the url 
    for the image to the database and redirects back to homepage.'''
    file = request.files['file']
    tagtext = request.form.get('tags')
    if file.filename == '' or tagtext == '':
        flash('Didn\'t submit required infromation!', category='error')
        return redirect(url_for('views.home'))
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
    meme = Meme(url=path,tags=tagtext, user_id=current_user.id, username=current_user.username)
    db.session.add(meme)
    db.session.commit()
    flash('Meme Succefully Uploaded!', category='success')
    return redirect(url_for('views.home'))

@views.route('/meme/<path:id>')
def view_meme(id):
    '''Gets the meme by its id then displays the meme page and 
    passes the meme data to the page'''
    meme = Meme.query.filter_by(id=id).first()
    memeT = MemeType(meme)
    return render_template('meme.html',meme=memeT)

@views.route('/like', methods=['POST'])
def like():
    if current_user.is_authenticated == True:
        meme_id = request.form.get('id')
        meme = Meme.query.filter_by(id=meme_id).first()
        liked = []
        if meme.liked != '':
            liked = json.loads(meme.liked)
        liked.append(current_user.id)
        meme.liked = json.dumps(liked)
        db.session.commit()
        return 'Success'
    else:
        return 'Login'

@views.route('/unlike', methods=['POST'])
def unlike():
    if current_user.is_authenticated == True:
        meme_id = request.form.get('id')
        meme = Meme.query.filter_by(id=meme_id).first()
        liked = json.loads(meme.liked)
        index = liked.index(current_user.id)
        del liked[index]
        meme.liked = json.dumps(liked)
        db.session.commit()
        return 'Success'
    else:
        return 'Login'

@views.route('/profile/<path:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    userT = UserType(user)
    return render_template('profile.html',user=userT)

@views.route('/search', methods=['POST'])
def search():
    '''Gets the string that the user would like to search with then 
    splits it into individual tags and searches the database for each tag.
    It combines each list of memes into one list and runs combine_memes and then 
    convert_to_memetype on the combined list and displays and passes the memes 
    to the search page.'''
    tags = request.form.get('search')
    if tags == '':
        flash('Invaild Search!', category='error')
        return redirect(url_for('views.home'))
    combined_memes = search(tags,1)
    memesT = convert_to_memetype(combined_memes)
    result = {'search': tags, 'memes': memesT}
    return render_template('search.html', res=result)

@views.route('/about')
def about():
    '''Displays the credits page'''
    return render_template('about.html')

@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

def search(tags, page_num):
    multi_memes = []
    for tag in tags.split():
        memes = Meme.query.filter(Meme.tags.contains(tag)).paginate(page=page_num,per_page=50).items
        multi_memes.append(memes)
    return combine_memes(multi_memes)
     
def convert_to_memetype(memes) -> list:
    '''Converts a list of memes from the database into a list of memes 
    of type MemeType.'''
    if len(memes) == 0:
        return []
    if len(memes) == 1:
        return [MemeType(memes[0])]
    meme = memes[0]
    del memes[0]
    return [MemeType(meme)] + convert_to_memetype(memes)

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

class MemeType():

    def __init__(self, meme):
        '''Takes a meme from the database and converts it into
        a MemeType object.'''
        self.id = meme.id
        self.url = meme.url
        tags = []
        for tag in meme.tags.split():
            tags.append(tag)
        self.tags = tags
        self.liked = []
        if meme.liked != '':
            self.liked = json.loads(meme.liked)
        self.likes = len(self.liked)
        self.user_id = meme.user_id
        self.username = meme.username
        self.date = meme.date.isoformat()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class UserType():

    def __init__(self, user):
        self.id = user.id
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.memes = convert_to_memetype(user.memes)
 