from functools import wraps
from jsonschema import validate, ValidationError
from flask import Blueprint, make_response, jsonify, request

from app import db
from registry.app.models import Service, Instance

registry_blueprint = Blueprint('registry', __name__)

register_schema = '''
{
  "name": "service",
  "port": "8080"
}
'''


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), schema)
            except ValidationError as e:
                return response(409, status='error',
                                reason='wrong json',
                                message=e.message)
            return f(*args, **kw)

        return wrapper

    return decorator


def response(code=200, **kwargs):
    rsp = jsonify(kwargs) if kwargs else ''
    return make_response(rsp), code


@registry_blueprint.route('/')
def tests():
    data = request.get_json()
    return response(data)


@registry_blueprint.route('/register')
@validate_schema(register_schema)
def register():
    host = request.host_url
    data = request.get_json()
    service = Service.query.filter_by(data.name).first()

    if service == 0:
        service = Service(data.name)
        db.session.add(service)

    instance = Instance(host, data.port, service.id)

    # TODO: make error exception
    db.session.add(instance)
    db.session.commit()

    return response(204)


@registry_blueprint.route('/unregister')
@validate_schema(register_schema)
def unregister():
    port = request.get_json().port
    host = request.host_url
    Instance.query.filter_by(port=port, host=host).delete()
    db.session.commit()
    return response(204)
