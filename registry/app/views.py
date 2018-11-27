from functools import wraps
from jsonschema import validate, ValidationError
from flask import Blueprint, make_response, jsonify, request, current_app

from app import db
from app.models import Service, Instance

registry_blueprint = Blueprint('registry', __name__)

register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "port": {"type": "string"}
    },
    "required": ["name", "port"]
}


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), schema)
            except ValidationError as e:
                return response(400, status='error',
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
    print(request.get_json())
    print(register_schema)
    print(validate(request.get_json(), register_schema))
    data = request.get_json()
    return response(data)


@registry_blueprint.route('/register')
@validate_schema(register_schema)
def register():
    host = request.remote_addr
    port = request.get_json().get('port')
    name = request.get_json().get('name')
    service = Service.query.filter_by(name=name).first()

    current_app.logger.info(f"Searching for service {name}, result: {service}")

    if not service:
        print('FUck')
        current_app.logger.info(f"No service with name {name} "
                                f"were found. Creating new one")
        service = Service(name)
        db.session.add(service)
        db.session.commit()

    service = Service.query.filter_by(name=name).first()

    instance = Instance(host, port, service.id)

    # TODO: make error exception
    db.session.add(instance)
    db.session.commit()

    return response(204)


@registry_blueprint.route('/unregister')
@validate_schema(register_schema)
def unregister():
    port = request.get_json().get('port')
    host = request.remote_addr
    Instance.query.filter_by(port=port, host=host).delete()
    db.session.commit()
    return response(204)


@registry_blueprint.route('/instances/<string:name>', methods=['GET'])
def instances(name):
    service = Service.query.filter_by(name=name).first()
    inst_list = Instance.query.filter_by(service_id=service.id).all()
    print(inst_list)
    inst = [x.as_dict() for x in inst_list]
    return response(200, instances=inst)
