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

# 如果是使用 flask-mail 但是使用 sengrid server 的話 -> "smtp.sendgrid.net", 那必需使用 TLS 而不是 SSL
# 目前在 Google Compute Engine 裡發信是使用 sengrid ! 所以 .env 目前是沒有設置 MAIL_USE_SSL 的
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') 

MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')

GCP_PROJECT_NAME = os.getenv('GCP_PROJECT_NAME')

GCP_SERVICE_ID_TOKEN = os.getenv('GCP_SERVICE_ID_TOKEN')

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
