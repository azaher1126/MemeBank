from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', DataRequired())
    last_name = StringField('Last Name', DataRequired())
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
        EqualTo('password', message='Confirmed password must match password.')])
    captcha = RecaptchaField()
    submit = SubmitField('Register')
