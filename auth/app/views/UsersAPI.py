from flask import request, current_app
from flask.views import MethodView
from sqlalchemy import exc

from . import create_response, validate_json, require_auth
from .. import db, bcrypt
from ..models import User

register_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'}
    },
    'required': ['username', 'password', 'email']
}

update_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'}
    }
}


class UsersAPI(MethodView):
    @staticmethod
    @require_auth()
    def get(username):
        """
        Returning user info object
        This request is 'self_only', the request can be executed only if the
        bearers's username is the same as the parameter `username`

        :param username: Username of user about whom info need to be returned
        :return: Returning user info structure or 404 if user not found, or 403
            if requesting info without authorization
        """
        current_app.logger.info('Attempt to get info about user')

        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = User.decode_auth_token(token)
        if payload['username'] != username:
            current_app.logger.info('Attempt rejected, wrong username')
            return create_response(403, status='error', message='forbidden')

        user = User.query.filter_by(username=username).first()
        if user is None:
            current_app.logger.info('Attempt rejected, no such user')
            return create_response(404, status='error', message='not found')

        user_dict = user.as_dict()
        user_dict.pop('password')
        current_app.logger.info('User info returned')
        return create_response(200, status='success', user_info=user_dict)

    @staticmethod
    @validate_json(register_schema)
    def post():
        """
        Creating a new user

        :return: Returning 200 and JWT if data is valid, 409 if user with such
            data is exists, or 422 if provided invalid JSON schema
        """
        current_app.logger.info('Attempt to register a new user')
        data = request.get_json()

        user = User(
            user=data.get('username'),
            password=data.get('password'),
            email=data.get('email')
        )
        db.session.add(user)

        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            current_app.logger.info('Rejecting attempt to create a new user. '
                                    'Such user already exists')
            return create_response(409, status='error', message='email taken')

        current_app.logger.info('New user created')
        token = user.encode_auth_token().decode()
        return create_response(200, jwt=token)

    @staticmethod
    @require_auth()
    @validate_json(update_schema)
    def put(username):
        # TODO: Implement roles logic, admins should be allowed to this method
        """
        Updating user info
        This request is 'self_only', the request can be executed only if the
        bearers's username is the same as the parameter `username`

        :param username: Username of user to update
        :return: Returning 204 if info updated or 409 if cannot update due
            conflict or 404 in there is no user with such username, or 403 if
            token is invalid
        """
        current_app.logger.info('Attempt to change user data')
        data = request.get_json()
        if 'password' in data:
            pw = data['password']
            data['password'] = bcrypt.generate_password_hash(pw, 5).decode()
        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = User.decode_auth_token(token)
        if payload['username'] == username:
            try:
                User.query.filter_by(username=username).update(data)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                current_app.logger.info('Attempt rejected. Data conflict')
                return create_response(409, status='error')
            current_app.logger.info('User data changed')
            return create_response()

        current_app.logger.info('Attempt rejected. Insufficient rights')
        return create_response(403, status='error', message='forbidden')

    @staticmethod
    @require_auth()
    def delete(username):
        # TODO: Implement roles logic, admins should be allowed to this method
        """
        Deleting user
        This request is 'self_only', the request can be executed only if the
        bearers's username is the same as the parameter `username`

        :param: username: Username of user to delete
        :return: Returning 204 if user deleted or 404 if there is no such user
            or 403 if client do not have rights to delete user
        """
        current_app.logger.info('Attempt to delete user')
        token = request.headers.get('Authorization').replace('Bearer ', '')
        payload = User.decode_auth_token(token)
        if payload['username'] == username:
            try:
                User.query.filter_by(username=username).delete()
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                current_app.logger.info('Attempt rejected. Data conflict')
                return create_response(400, status='error')
            current_app.logger.info('User deleted')
            return create_response()

        current_app.logger.info('Attempt rejected. Insufficient rights')
        return create_response(403, status='error', message='forbidden')
