import secrets


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = str(secrets.token_urlsafe(1024))
    LENGTH_SHORTEN = 10
    SESSION_COOKIE_SECURE = True
    FLASK_ADMIN_SWATCH = "cerulean"
    SECURITY_PASSWORD_SALT = None
    SECURITY_REGISTERABLE = False


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/sqlite/site.db"
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    TESTING = True
    SESSION_COOKIE_SECURE = False
