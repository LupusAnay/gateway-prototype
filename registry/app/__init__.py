from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)

    db.init_app(app)

    from registry.app.views import registry_blueprint
    app.register_blueprint(registry_blueprint)
    return app
