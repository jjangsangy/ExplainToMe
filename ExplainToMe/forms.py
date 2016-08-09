from wtforms.fields.html5 import IntegerField, URLField
from wtforms.validators import DataRequired, number_range, url


class LinkForm():
    url = URLField('url', validators=[DataRequired(), url()])
    max_sent = IntegerField('max_sent', validators=[DataRequired(),
                                                    number_range(min=0, max=100)])
