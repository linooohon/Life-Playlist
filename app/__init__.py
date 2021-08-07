import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail


from app.config.config import config
from app.settings import choose_db, FLASK_ENV

db = SQLAlchemy()
cache = Cache()
mail = Mail()
DB_NAME = choose_db(FLASK_ENV)


def create_app(config_name):
    app = Flask(__name__)

    # 1. 普通直接設置方式
    # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/logintodo_dev'

    # print("===========")
    # print(config_name)
    # print(DB_NAME)
    # print("===========")

    # 2. 採用 config.py 設置，多了架構，擴充性
    app.config.from_object(config[config_name])

    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)

    from app.views.views import views
    from app.views.auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from app.model.models import User, Playlist

    # create_database(app)

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


# 不確定是不是只給 SQLlite 使用
# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
