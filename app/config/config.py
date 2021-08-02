import os
# import datetime
# import pymysql

from app.settings import (
    SECRET_KEY, FLASK_ENV, choose_db, 
    MYSQL_CONNECTION_DEV, POSTGRESQL_CONNECTION_PRO,
    POSTGRESQL_CONNECTION_DEV_DOCKER
    )

# 拿當下絕對路徑 -> 在這裡的話也就是 /Users/linpinhung/XXX/life-playlist/app/config
basedir = os.path.abspath(os.path.dirname(__file__))

# 根據 dev pro test 切換 db
DB_NAME = choose_db(FLASK_ENV)


def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)


class BaseConfig(object):  # 基底，共用的
    DEBUG = False
    TESTING = False

# 以下都繼承 Base


class ProductionConfig(BaseConfig):
    SECRET_KEY = SECRET_KEY

    # Flask-sqlalchemy
    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_CONNECTION_PRO
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = SECRET_KEY

    ENV = "development"
    DEBUG = True

    # Flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = MYSQL_CONNECTION_DEV
    # SQLALCHEMY_DATABASE_URI = create_sqlite_uri(DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'simple'
    # CACHE_REDIS_HOST = '127.0.0.1'
    # CACHE_REDIS_PORT = 6379


class DockerDevelopmentConfig(BaseConfig):
    SECRET_KEY = SECRET_KEY

    ENV = "development"
    DEBUG = True

    # Flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_CONNECTION_DEV_DOCKER
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    SECRET_KEY = SECRET_KEY
    ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri(DB_NAME)


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
    "development_docker": DockerDevelopmentConfig,
}
