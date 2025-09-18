from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired()], render_kw={"placeholder": "Enter your first name"})
    last_name = StringField('Last Name', [DataRequired()], render_kw={"placeholder": "Enter your last name"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter a username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email address"})
    password = PasswordField('Password', validators=[DataRequired(), Length(7, message='Password must be at least 7 characters')], render_kw={"placeholder": "Enter a password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
        EqualTo('password', message='Confirmed password must match password.')], render_kw={"placeholder": "Enter password again"})
    captcha = RecaptchaField("Recaptcha", validators=[Recaptcha(message="The recaptcha field must be completed.")])
    submit = SubmitField('Register')
