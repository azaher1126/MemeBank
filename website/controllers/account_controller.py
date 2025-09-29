from sqlalchemy import or_, and_, desc, func
from flask import Blueprint, render_template, request, redirect, flash, abort, send_from_directory
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import url_for
from ..database.user_model import User
from ..database.meme_model import Meme
from ..database import db
from ..models.user_model import UserType
from ..models.meme_model import convert_to_memetype
from ..forms.login_form import LoginForm
from ..forms.register_form import RegisterForm
from ..forms import flash_errors
from ..uploads.profile_uploads import profile_uploads
from .helpers.anonymous_only import anonymous_only
from .helpers.login_helpers import is_login_required, login_required

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register():
    register_form: RegisterForm = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        email_lowered = email.lower()
        username = register_form.username.data
        username_lowered = username.lower()
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        password = register_form.password.data

        existing_user = db.session.query(User).filter(or_(func.lower(User.email) == email_lowered, func.lower(User.username) == username_lowered)).one_or_none()
        if existing_user:
            if existing_user.email.lower() == email_lowered:
                flash('Email already belongs to an account, login instead.', category='error')
            else:
                flash('Username already exists, please choose another one.', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f'Welcome {first_name}, your account has been created!', category='success')

            next_url = request.args.get('next')
            return redirect(next_url or url_for('public.home'))
    else:
        flash_errors(register_form)
    return render_template("account/register.html", register_form=register_form)

@account_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    login_form: LoginForm = LoginForm(formdata=request.form)
    if login_form.validate_on_submit():
        email = login_form.username_or_email.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data
        user = User.query.filter(or_(func.lower(User.email)==email.lower(), func.lower(User.username)==email.lower())).one_or_none()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Welcome {user.first_name}, you have logged in successfully!", category='success')
                login_user(user, remember=remember_me)
                next_url = request.args.get('next')
                return redirect(next_url or url_for('public.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email or username does not exist.', category='error')
    else:
        flash_errors(login_form)
    return render_template("account/login.html", login_form=login_form)

@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", 'success')
    next_url = request.args.get('next')
    redirect_url = next_url if next_url and not is_login_required(next_url) else url_for('public.home')
    return redirect(redirect_url)

@account_blueprint.route('/forget_password')
@anonymous_only
def forget_password():
    return render_template('account/forget_password.html')

@account_blueprint.route('/profile/<path:username>')
def profile(username):
    user = db.session.query(User).filter(func.lower(User.username)==username.lower()).first()
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

@account_blueprint.route('/profile/image/<path:id>')
def get_profile_image(id):
    user = db.session.query(User).filter(User.id == id).first()
    if not user:
        abort(404)
    if not user.profile_url:
        return send_from_directory('assets', 'default_profile.jpg')
    else:
        return send_from_directory(profile_uploads.config.destination, user.profile_url)
