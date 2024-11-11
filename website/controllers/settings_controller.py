from flask import Blueprint, render_template, request, abort
from flask_login import login_required
from ..database import db

settings_blueprint = Blueprint('settings', __name__, url_prefix='/settings')

@settings_blueprint.route('/profile')
@login_required
def profile_settings():
    '''Displays the profile settings page'''
    return render_template("settings/profile_settings.html")

@settings_blueprint.route('/account')
@login_required
def account_settings():
    '''Displays the account settings page'''
    return render_template("settings/account_settings.html")
