from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from gateway.app.views import Service

    services = [Service('http://localhost:8000/', 'service', 'some_service_1'),
                Service('http://localhost:8002/', 'service', 'some_service_2'),
                Service('http://localhost:8001/', 'auth', 'auth_service')]

    for service in services:
        app.register_blueprint(service.blueprint)

    return app
