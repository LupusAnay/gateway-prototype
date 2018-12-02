import requests

from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from serivce.app.views import service_blueprint
    app.register_blueprint(service_blueprint)

    return app
