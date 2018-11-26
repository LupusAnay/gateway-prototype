from flask import Blueprint, request, make_response, jsonify
import neo4j as neo

bp = Blueprint('movies', __name__)


@bp.route('/movies', methods=['POST'])
def root():
    post_data = request.get_json()

    return make_response(jsonify('hello')), 200

