import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from app.config.config import config
from app.settings import DB_NAME

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # 1. 普通直接設置方式
    # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # print("===========")
    # print(config_name)
    # print(DB_NAME)
    # print("===========")

    # 2. 採用 config.py 設置，多了架構，擴充性
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.views.views import views
    from app.views.auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from app.model.models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # print("================")
    # print(os.path.dirname(__file__))
    # print(os.path.abspath(__file__))
    # print(basedir)
    # print("================")

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
