from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView

from . import db, bcrypt
from .models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def root():
    username = request.args.get('username')
    password = request.args.get('password')

    user = User.query.filter_by(user=username).first()

    result = bcrypt.check_password_hash(user.password, password)
    return make_response(jsonify(result)), 200


class RegisterAPI(MethodView):
    @staticmethod
    def post():
        post_data = request.get_json()

        user = User(
            user=post_data.get('user'),
            password=post_data.get('password'),
            email=post_data.get('email'),
            role=post_data.get('role')
        )

        db.session.add(user)
        db.session.commit()

        response = {
            'result': 'success',
            'token': str(user.encode_auth_token(user.id,
                                                post_data.get('role')))
        }

        return make_response(jsonify(response)), 200


registration_view = RegisterAPI.as_view('register_api')

auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)
