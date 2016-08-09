"""
Neural Poet
===========
"""
import os

from flask import Flask
from flask_assets import Environment
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_heroku import Heroku

from .views.site import site

__title__ = 'ExplainToMe'
__license__ = 'Apache Software License Version 2.0'

app = Flask(__name__)

app.register_blueprint(site)

cors = CORS(app)
bootstrap = Bootstrap(app)
heroku = Heroku(app)
environment = Environment(app)
