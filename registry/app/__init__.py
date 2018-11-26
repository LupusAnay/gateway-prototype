from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from registry.app.views import registry_blueprint
    app.register_blueprint(registry_blueprint)
    return app
