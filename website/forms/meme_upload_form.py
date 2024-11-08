from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from ..uploads.meme_uploads import meme_uploads

class MemeUploadForm(FlaskForm):
    meme = FileField('Choose image', validators=[FileRequired(), FileAllowed(meme_uploads, 'Images only!')])
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Upload')
