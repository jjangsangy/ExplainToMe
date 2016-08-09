from wtforms.fields.html5 import IntegerField, URLField
from wtforms.validators import number_range, url


class LinkForm():
    url = URLField(validators=[url()])
    max_sent = IntegerField(validators=[number_range(min=0, max=100)])
