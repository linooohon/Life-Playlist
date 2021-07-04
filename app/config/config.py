import os
import datetime
from app.settings import SECRET_KEY, DB_NAME

basedir = os.path.abspath(os.path.dirname(__file__))

def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(BaseConfig):
    SECRET_KEY = SECRET_KEY

    # Flask-sqlalchemy
    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri(DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = SECRET_KEY

    # Flask-sqlalchemy
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@ip:3306/tablename'
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri(DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(BaseConfig):
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
