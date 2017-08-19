from flask_wtf import FlaskForm as Form
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.fields import SelectField
from wtforms.validators import NumberRange, InputRequired
from wtforms.validators import URL, Required


class LinkForm(Form):

    url = URLField(
        'url',
        validators=[Required(), InputRequired(), URL()],
        id='url',
        render_kw={'placeholder': 'URL https://...'}
    )
    max_sent = IntegerField(
        'max_sent',
        validators=[Required(), InputRequired(), NumberRange(min=0, max=100)],
        id='max_sent',
        default=10
    )
    language = SelectField(
        'language',
        validators=[Required(), InputRequired()],
        id='language',
        choices=[('english','English'), ('chinese', 'Chinese'), ('czech', 'Czech'), ('french', 'French'), ('german', 'German'), ('japanese', 'Japanese'), ('portuguese', 'Portuguese'), ('slovak', 'Slovak'), ('spanish', 'Spanish')],
        default='english'
    )
