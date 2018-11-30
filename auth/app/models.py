import jwt

from sqlalchemy import inspect
from datetime import datetime, timedelta
from flask import current_app

from . import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, user, password, email, role='user'):
        self.username = user
        self.password = bcrypt.generate_password_hash(password, 5).decode()
        self.email = email
        self.role = role
        self.registered_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    # TODO: Implement role functional
    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
                'iat': datetime.utcnow(),
                'user_id': self.id,
                'username': self.username,
                'user_role': self.role
            }
            return jwt.encode(payload,
                              current_app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,
                                 current_app.config.get('SECRET_KEY'),
                                 algorithm='HS256')
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
