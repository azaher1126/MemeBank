from sqlalchemy import or_, and_, desc
from flask import Blueprint, render_template, request, redirect, flash, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import url_for
from ..database.user_model import User
from ..database.meme_model import Meme
from ..database import db
from ..models.user_model import UserType
from ..models.meme_model import convert_to_memetype
from .helpers.anonymous_only import anonymous_only

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
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
            login_user(new_user)
            flash('Account created!', category='success')

            next_url = request.args.get('next')
            return redirect(next_url or url_for('public.home'))

    return render_template("account/register.html")

@account_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
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
                next_url = request.args.get('next')
                return redirect(next_url or url_for('public.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("account/login.html")

@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", 'success')
    next_url = request.args.get('next')
    return redirect(next_url or url_for('public.home'))

@account_blueprint.route('/forget_password')
@anonymous_only
def forget_password():
    return render_template('account/forget_password.html')

@account_blueprint.route('/profile/<path:username>')
def profile(username):
    user = db.session.query(User).filter(User.username==username).first()
    if not user:
        abort(404)
    last_id = request.args.get('last_id')
    if not last_id:
        memes = db.session.query(Meme).filter(Meme.user_id==user.id).order_by(desc(Meme.date)).limit(20).all()
        userT = UserType(user, memes)
        return render_template('account/profile.html',user=userT)
    # Page is requesting more memes
    last_meme = db.session.query(Meme).filter(Meme.id == last_id).first()
    if not last_meme:
        abort(404)
    memes = db.session.query(Meme).order_by(desc(Meme.date)).filter(and_(Meme.id < last_meme.id, Meme.user_id==user.id)).limit(20).all()
    memesT = convert_to_memetype(memes)
    return render_template('components/meme_page.html', memes=memesT)

@account_blueprint.route('/settings')
@login_required
def settings():
    return render_template('account/settings.html')