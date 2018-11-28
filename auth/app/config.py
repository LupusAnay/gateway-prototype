import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_user = os.getenv('DB_USER', 'postgres')
db_pw = os.getenv('DB_PASS', 'postgres')
db_name = os.getenv('DB_NAME', 'postgres')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

postgre_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
sqlite_db = 'sqlite:////tmp/auth.db'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = sqlite_db


class TestingConfig(BaseConfig):
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = postgre_url
