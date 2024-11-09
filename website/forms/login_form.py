from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username_or_email = StringField('Email/Username', validators=[DataRequired()], render_kw={"placeholder": "Enter your email or username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
