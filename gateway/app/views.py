import requests
from flask import Blueprint, make_response, request


class Service:
    def __init__(self, host, proxy_route, name):
        self.blueprint = Blueprint(name, __name__)
        self.host = host
        self.name = name
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']

        @self.blueprint.route(f'/{proxy_route}/',
                              defaults={'path': ''},
                              methods=self.methods)
        @self.blueprint.route(f'/{proxy_route}/<path:path>',
                              methods=self.methods)
        def service_request(path):
            print('Making post request to:', f'{self.host}{path}')
            resp = requests.request(
                method=request.method,
                url=f'{self.host}{path}',
                headers={key: value for (key, value) in request.headers if
                         key != 'Host'},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
            return make_response(resp.content)
