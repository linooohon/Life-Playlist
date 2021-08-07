import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_ENV = os.getenv('FLASK_ENV')
MYSQL_CONNECTION_DEV = os.getenv('MYSQL_CONNECTION_DEV')
POSTGRESQL_CONNECTION_DEV_DOCKER = os.getenv('POSTGRESQL_CONNECTION_DEV_DOCKER')
POSTGRESQL_CONNECTION_PRO = os.getenv('POSTGRESQL_CONNECTION_PRO')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

def choose_db(config_name):
    if config_name == 'production':
        DB_NAME = os.getenv('DB_NAME_PRO')
    elif config_name == 'testing':
        DB_NAME = os.getenv('DB_NAME_TEST')
    elif config_name == 'development_docker':
        DB_NAME = os.getenv('DB_NAME_DEV_DOCKER')
    else:
        DB_NAME = os.getenv('DB_NAME_DEV')
    return DB_NAME
