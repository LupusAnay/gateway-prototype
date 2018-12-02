from flask import Blueprint, make_response, jsonify, request
from functools import wraps
from serivce.jwt_decoder import decode_auth_token

service_blueprint = Blueprint('service', __name__, url_prefix='/service')


def require_auth(role=''):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            token = request.headers.get('Authorization').replace('Bearer ', '')
            payload = decode_auth_token(token)
            print(payload)
            if type(payload) is not dict:
                return make_response(jsonify({'error': 'token_error',
                                              'token': payload}))
            return f(*args, **kwargs)

        return wrapped_f

    return wrap


@service_blueprint.route('/')
@require_auth(role='fuck')
def get():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    data = decode_auth_token(token)
    print('im here')
    response = {
        'result': 'success',
        'secret_resource': 'hello from hell',
        'token': data
    }
    print('im after token decoding', response)
    return make_response(jsonify(response)), 200
