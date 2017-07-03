# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_appconfig import AppConfig
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from flask_heroku import Heroku
from flask_sslify import SSLify

from . version import __version__ as version

from . filters import datetimefilter
from . error import error_not_found
from . config import config_env_files


def load_extensions(app):
    Bootstrap(app)
    AppConfig(app)
    Heroku(app)
    CORS(app)
    DebugToolbarExtension(app)
    CSRFProtect(app)
    SSLify(app)

def register_blueprints(app):
    from . views import root, api
    app.register_blueprint(root)
    app.register_blueprint(api,
        url_prefix='/api/v{version}'.format(version=version))

def register_handlers(app):
    app.register_error_handler(404, error_not_found)
    app.jinja_env.filters['datetimefilter'] = datetimefilter


def create_app(default_config='dev'):
    app = Flask(__name__, static_url_path='')

    app.config.from_object(
        config_env_files.get(os.getenv('APP_SETTINGS', default_config))
    )
    app.secret_key = app.config['SECRET_KEY']
    # Apply from [left -> right]
    for f in [load_extensions, register_blueprints, register_handlers]:
        f(app)
    return app
