from functools import wraps
from jsonschema import validate, ValidationError
from flask import Blueprint, make_response, jsonify, request, current_app
from flask.views import MethodView
from app import db
from app.models import Service, Instance

instance_blueprint = Blueprint('registry', __name__)

register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "port": {"type": "string"}
    },
    "required": ["name", "port"]
}


def response(code=200, **kwargs):
    rsp = jsonify(kwargs) if kwargs else ''
    return make_response(rsp), code


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), schema)
            except ValidationError as e:
                print(e.message)
                return response(400, status='error',
                                reason='wrong json',
                                message=e.message)
            return f(*args, **kw)

        return wrapper

    return decorator


class InstanceAPI(MethodView):
    @staticmethod
    def get(name):
        service = Service.query.filter_by(name=name).first()
        inst_list = Instance.query.filter_by(service_id=service.id).all()
        print(inst_list)
        inst = [x.as_dict() for x in inst_list]
        return response(200, instances=inst)

    @staticmethod
    @validate_schema(register_schema)
    def post():
        host = request.remote_addr
        port = request.get_json().get('port')
        name = request.get_json().get('name')
        service = Service.query.filter_by(name=name).first()

        current_app.logger.info(
            f"Searching for service {name}, result: {service}")

        if not service:
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

    @staticmethod
    @validate_schema(register_schema)
    def delete():
        port = request.get_json().get('port')
        host = request.remote_addr
        Instance.query.filter_by(port=port, host=host).delete()
        db.session.commit()
        return response(204)


instance_view = InstanceAPI.as_view('register_api')

instance_blueprint.add_url_rule('/instance',
                                view_func=instance_view,
                                methods=['POST', 'DELETE'])

instance_blueprint.add_url_rule('/instance/<string:name>',
                                view_func=instance_view,
                                methods=['GET'])
