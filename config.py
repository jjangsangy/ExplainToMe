import os
import binascii

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    ASSETS_DEBUG = True
    SECRET_KEY = binascii.hexlify(os.urandom(24))


class ProductionConfig(BaseConfig):
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
