from sqlalchemy import or_
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask.helpers import url_for
from ..database.user_model import User
from ..database import db
from ..models.user_model import UserType

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('public.home'))

    return render_template("account/register.html")

@account_blueprint.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('public.home'))
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
    return redirect(url_for('public.home'))

@account_blueprint.route('/forget_password')
def forget_password():
    return render_template('account/forget_password.html')

@account_blueprint.route('/profile/<path:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    userT = UserType(user)
    return render_template('account/profile.html',user=userT)

@account_blueprint.route('/settings')
@login_required
def settings():
    return render_template('account/settings.html')