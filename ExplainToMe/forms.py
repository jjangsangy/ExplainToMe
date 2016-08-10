from flask_wtf import Form
from flask_wtf.html5 import URLField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import URL, DataRequired, number_range


class LinkForm(Form):
    url = URLField('url', render_kw={
        'class': 'form-control',
        'placeholder': 'Summary URL',
        'required': True,
    }, id='url',
        validators=[DataRequired(), URL()])
    max_sent = IntegerField('max_sent', render_kw={
        'class': 'form-control',
        'placeholder': 'Max Sentences',
        'required': True,
    }, id='max_sent',
        default=10,
        validators=[DataRequired(), number_range(min=0, max=100)]
    )
