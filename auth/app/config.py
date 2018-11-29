import os

basedir = os.path.abspath(os.path.dirname(__file__))

pg_user = os.getenv('DB_USER', 'postgres')
pg_pw = os.getenv('DB_PASS', 'postgres')
pg_name = os.getenv('DB_NAME', 'postgres')
pg_host = os.getenv('DB_HOST', 'localhost')
pg_port = os.getenv('DB_PORT', '5432')

postgre_url = f"postgresql://{pg_user}:{pg_pw}@{pg_host}:{pg_port}/{pg_name}"
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
