"""
ExplainToMe
===========
"""
import os

from dateutil.parser import parser
from flask import Flask
from flask_assets import Environment
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_heroku import Heroku
from flask_wtf import CsrfProtect
from flaskext.markdown import Markdown

from .views.site import site

__title__ = 'ExplainToMe'
__license__ = 'Apache Software License Version 2.0'

app = Flask(__name__)

app.register_blueprint(site)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'w+sJMWsCKSCyfZ0eUGWaYALzIc78zFVs')


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    p = parser()
    dt = p.parse(value)
    return dt.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

cors = CORS(app)
bootstrap = Bootstrap(app)
heroku = Heroku(app)
environment = Environment(app)
csrfprotect = CsrfProtect(app)
markdown = Markdown(app)
