from flask import flash, Flask
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def initialize_forms(app: Flask):
    csrf.init_app(app)

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')