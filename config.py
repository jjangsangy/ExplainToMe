import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    ASSETS_DEBUG = True
    MESSENGER_APP_SECRET = None
    MESSENGER_VALIDATION_TOKEN = None
    PAGE_ACCESS_TOKEN = None
    SERVER_URL = None
    VALIDAYION_TOKEN = None


class ProductionConfig(BaseConfig):
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
