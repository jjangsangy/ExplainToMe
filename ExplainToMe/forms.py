from flask_wtf import FlaskForm as Form
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.validators import NumberRange, InputRequired
from wtforms.validators import URL, Required


class LinkForm(Form):

    url = URLField(
        'url',
        validators=[Required(), InputRequired(), URL()],
        id='url',
    )
    max_sent = IntegerField(
        'max_sent',
        validators=[Required(), InputRequired(), NumberRange(min=0, max=100)],
        id='max_sent',
        default=10,
    )
