"""
ExplainToMe
===========
"""
import logging
import os

from dateutil.parser import parser
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_heroku import Heroku
from flask_wtf import CsrfProtect
from mashapeanalytics.middleware import FlaskMiddleware as MashapeAnalytics

from .views.site import site

__title__ = 'ExplainToMe'
__license__ = 'Apache Software License Version 2.0'


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

mashape = os.getenv("MASHAPE_GALILEO", '')
if mashape:
    app.wsgi_app = MashapeAnalytics(
        app.wsgi_app,
        mashape,
        'default-environment',
    )

app.register_blueprint(site)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',
                                     'v8iqZjndP7dtZuqnkttGgqlszSEDWnI8')
app.config.from_object(os.getenv('APP_SETTINGS',
                                 'config.DevelopmentConfig'))


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    p = parser()
    dt = p.parse(value)
    return dt.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

cors = CORS(app)
bootstrap = Bootstrap(app)
heroku = Heroku(app)
