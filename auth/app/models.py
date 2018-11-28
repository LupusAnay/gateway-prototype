import jwt

from datetime import datetime, timedelta
from flask import current_app

from . import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, user, password, email, role):
        self.user = user
        self.password = bcrypt.generate_password_hash(password, 5).decode()
        self.email = email
        self.role = role
        self.registered_on = datetime.now()

    # For Prototype. Need proper role realization
    # TODO: DO NOT FORGET ABOUT ROLE
    @staticmethod
    def encode_auth_token(user_id, role):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
                'iat': datetime.utcnow(),
                'sub': user_id,
                'role': role
            }
            return jwt.encode(payload,
                              current_app.config.get['SECRET_KEY'],
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,
                                 current_app.config.get['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
