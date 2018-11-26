from flask import Blueprint, make_response, jsonify


registry_blueprint = Blueprint('registry', __name__)


def response(code=200, **kwargs):
    return make_response(jsonify(kwargs)), code


@registry_blueprint.route('/')
def root():
    return response(300, fuck='you', why='because')
