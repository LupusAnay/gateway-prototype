import requests
from flask import Blueprint, make_response, request

proxy_blueprint = Blueprint('proxy', __name__)

app_methods = ['GET', 'POST', 'PUT', 'DELETE']


@proxy_blueprint.route('/<string:name>/', defaults={'path': ''},
                       methods=app_methods)
@proxy_blueprint.route('/<string:name>/<path:path>',
                       methods=app_methods)
def service_request(name, path):

    instances = requests.get(f'http://localhost:5000/instance/{name}')
    data = instances.json()

    instance = data.get('instances')[0]

    resp = requests.request(
        method=request.method,
        url=f"http://{instance.get('host')}:{instance.get('port')}/{path}",
        headers={key: value for key, value in request.headers
                 if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False)

    return make_response(resp.content, resp.status_code)
