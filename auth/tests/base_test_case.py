from flask import current_app
from flask_testing import TestCase

from auth.app import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('auth.app.config.TestingConfig')

    def setUp(self):
        db.drop_all()
        current_app.logger.info('Creating database')
        db.create_all()
        db.session.commit()

    def tearDown(self):
        current_app.logger.info('Dropping database')
        db.session.remove()
        db.drop_all()
