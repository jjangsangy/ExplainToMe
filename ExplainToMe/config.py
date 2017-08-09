import os
import operator
import binascii

__all__ = ['config_env_files']

basedir = os.path.abspath(os.path.dirname(__file__))

def random_key(size):
    decoder = operator.methodcaller('decode')
    return decoder(binascii.hexlify(os.urandom(size)))

def environment_name(pyobj):
    return '.'.join(['ExplainToMe', 'config', pyobj])

class Base(object):
    BOOTSTRAP_QUERYSTRING_REVVING = False
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_USE_MINIFIED = False
    DEBUG = True
    JSON_AS_ASCII = False
    MAX_FILE_SIZE = 1024 * 1024 + 1
    APPLICATION_ROOT = '/'
    SECRET_KEY = os.getenv('SECRET_KEY', random_key(24))


class Development(Base):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEVELOPMENT = True
    TESTING = False
    WTF_CSRF_SSL_STRICT = False
    WTF_CSRF_CHECK_DEFAULT = False


class Testing(Base):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = 'test'
    TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_SESSION_KEY = 'test-session'


class Production(Base):
    DEBUG = False
    DEVELOPMENT = False
    SERVER_NAME = os.getenv('SERVER_NAME')
    TESTING = False
    WTF_CSRF_ENABLED = False


config_env_files = {
    'prod': environment_name('Production'),
    'dev': environment_name('Development'),
    'test': environment_name('Testing')
}
