from flask import Blueprint, Response, make_response, jsonify, request, \
    current_app
from jsonschema import validate, ValidationError
from functools import wraps

from ..models import User


def require_auth(role='user'):
    # TODO: Implement proper roles check
    """
    Checks JWT from request 'Authorization' header

    WARN: roles not implemented

    :param: role: role that required to proceed request
    :return: Returning 403 error if token is not valid, otherwise executes
        decorated function
    """

    def wrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            current_app.logger.info('Attempt to access to protected resource')
            header = request.headers.get('Authorization')
            if header is not None:
                token = header.replace('Bearer ', '')
                payload = User.decode_auth_token(token)
                if type(payload) is dict:
                    current_app.logger.info('Access granted')
                    return f(*args, **kwargs)

            current_app.logger.info('Attempt rejected, invalid token')
            return create_response(403, status='error', message='forbidden')

        return wrapped_f

    return wrap


def create_response(code=204, **kwargs) -> Response:
    """
    Creating JSON response from key word arguments

    :param code: Status code of response
    :param kwargs: key=value args to create json with
    :return: Response object with given status code and arguments
    """
    return make_response(jsonify(kwargs), code)


def validate_json(schema):
    """
    Validating JSON from request, comparing it with given JSON schema

    :param schema: JSON Schema to compare it with request's
    :return:
        Response with status code 422 if JSON is invalid or result of
        decorated function json is valid
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), schema)
            except ValidationError as e:
                current_app.logger.info(
                    f'User provided wrong json schema: {request.get_json()}')
                return create_response(422, status='error',
                                       reason='Invalid json',
                                       message=e.message)
            return func(*args, **kw)

        return wrapper

    return decorator


users_blueprint = Blueprint('auth', __name__)
session_blueprint = Blueprint('session', __name__)

from .SessionAPI import SessionAPI
from .UsersAPI import UsersAPI

session_api = SessionAPI.as_view('session_api')
users_api = UsersAPI.as_view('users_api')

users_blueprint.add_url_rule(
    '/users',
    view_func=users_api,
    methods=['POST']
)

users_blueprint.add_url_rule(
    '/users/<string:username>',
    view_func=users_api,
    methods=['GET', 'PUT', 'DELETE']
)

session_blueprint.add_url_rule(
    '/session',
    view_func=session_api
)
