from flask import request, current_app
from flask.views import MethodView

from .. import bcrypt
from ..models import User
from . import validate_json, create_response, require_auth

login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}


class SessionAPI(MethodView):
    @staticmethod
    @validate_json(login_schema)
    def post():
        """
        Post method

        Accepting user's username and password
        Creating JWT for user

        :return: Returning auth token in credentials are valid, else returning
            404 error. If provided JSON is invalid returning 422
        """
        username = request.get_json().get('username')
        password = request.get_json().get('password')

        user = User.query.filter_by(username=username).first()

        if user is not None:
            if bcrypt.check_password_hash(user.password, password):
                token = user.encode_auth_token().decode()
                current_app.logger.info('Detected user login')
                return create_response(code=200, token=token)

        current_app.logger.info("User's login rejected")
        return create_response(code=404,
                               status='error',
                               message='Credentials rejected')

    @staticmethod
    @require_auth()
    def delete(token_data=None):
        # TODO: Implement token invalidation
        #  in microservice structure token invalidation need to be implemented
        #  on API gateway level, but token blacklisting won't be redundant
        """
        ---NOT IMPLEMENTED---
        Blacklisting user's token.
        :return: Returning 403 if token is invalid
        """
        current_app.logger.warn('Attempt to logout. '
                                'Not implemented, request has no effect')
        return create_response(202, status='none')
