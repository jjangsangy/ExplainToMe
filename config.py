import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    ASSETS_DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
