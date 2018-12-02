from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from gateway.app.views import proxy_blueprint
    app.register_blueprint(proxy_blueprint)

    return app
