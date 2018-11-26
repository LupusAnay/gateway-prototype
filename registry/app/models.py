from registry.app import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Instance(db.Model):
    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer,
                           db.ForeignKey('service.id'),
                           nullable=False)
    host = db.Column(db.String, nullable=False, default='http://localhost')
    port = db.Column(db.Integer, nullable=False)

    service = db.relationship('Service',
                              backref=db.backref('posts', lazy=True))

    def __init__(self, host, port, service_id):
        self.host = host
        self.port = port
        self.service_id = service_id
