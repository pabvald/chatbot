import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    MONITORING = False
    SECRET_KEY = 'some-strange-string'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    MONITORING = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONITORING = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONITORING = True


class TestingConfig(Config):
    TESTING = True
    MONITORING = True