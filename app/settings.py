import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_ENV = os.getenv('FLASK_ENV')
MYSQL_CONNECTION_DEV = os.getenv('MYSQL_CONNECTION_DEV')
POSTGRESQL_CONNECTION_PRO = os.getenv('POSTGRESQL_CONNECTION_PRO')

def choose_db(config_name):
    if config_name == 'production':
        DB_NAME = os.getenv('DB_NAME_PRO')
    elif config_name == 'testing':
        DB_NAME = os.getenv('DB_NAME_TEST')
    else:
        DB_NAME = os.getenv('DB_NAME_DEV')
    return DB_NAME
