import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_filename='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    CORS(app)

    app_settings = os.getenv(
        'APP_SETTINGS',
        config_filename
    )
    app.config.from_object(app_settings)

    bcrypt.init_app(app)
    db.init_app(app)

    from .views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
