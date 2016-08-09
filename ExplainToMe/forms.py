from wtforms.fields.html5 import URLField
from wtforms.validators import url


class LinkForm():
    url = URLField(validators=[url()])
    
