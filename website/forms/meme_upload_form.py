from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json

from ..uploads.meme_uploads import meme_uploads

class MemeUploadForm(FlaskForm):
    meme = FileField('Choose image', validators=[FileRequired(), FileAllowed(meme_uploads.extensions, 'Images only!')])
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meme.render_kw = dict(accept=','.join([f".{ext}" for ext in meme_uploads.extensions]))

    def get_tags(self):
        if not self.tags.validate(self):
            raise RuntimeError("Form does not contain valid data. Cannot retrieve tags.")
        tags_data = json.loads(self.tags.data) # type: ignore
        return [tag_data["value"] for tag_data in tags_data]
