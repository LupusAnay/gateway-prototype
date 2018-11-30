import json

from flask import Response, current_app
from .base_test_case import BaseTestCase


def register_user(self, username, password, email) -> Response:
    response = self.client.post("/users",
                                data=json.dumps(dict(username=username,
                                                     password=password,
                                                     email=email)
                                                ),
                                content_type='application/json')
    return response


class TestCreateUser(BaseTestCase):
    def test_registration(self):
        response = register_user(self, 'user', 'password', 'email@example.com')
        current_app.logger.info(response)

        self.assert200(response)

        data = json.loads(response.data.decode())

        self.assertTrue(data.get('jwt') is not None)

    def test_registration_with_already_registered_user(self):
        register_user(self, 'user', 'password', 'email@example.com')
        response = register_user(self, 'user', 'password', 'email@example.com')

        self.assertEqual(response.status_code, 409)

        current_app.logger.info(response)
        data = json.loads(response.data.decode())

        self.assertTrue(data is not None)
        self.assertEqual(data['status'], 'error')
