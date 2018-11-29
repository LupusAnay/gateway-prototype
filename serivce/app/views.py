from flask import Blueprint, make_response, jsonify, request
from functools import wraps
from serivce.jwt_decoder import decode_auth_token

service_blueprint = Blueprint('service', __name__)


def require_auth(role=''):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            payload = decode_auth_token(request.headers.get('Authorization'))
            if type(payload) is not dict:
                return make_response(jsonify({'error': 'token_error',
                                              'token': payload}))

            token_role = payload['role']
            print(token_role, role)
            if token_role != role:
                return make_response(jsonify({'error': 'role_error',
                                              'token': payload}))
            return f(*args, **kwargs)

        return wrapped_f

    return wrap


@service_blueprint.route('/')
@require_auth(role='fuck')
def get():
    token = request.headers.get('Authorization')
    print('im here')
    response = {
        'result': 'success',
        'secret_resource': 'hello from hell',
        'token': decode_auth_token(token)
    }
    print('im after token decoding', response)
    return make_response(jsonify(response)), 200
