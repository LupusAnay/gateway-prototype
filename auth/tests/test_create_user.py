import json

from flask import current_app
from auth.tests.base_test_case import BaseTestCase
from auth.tests.api_methods import register_user


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

    def test_register_with_invalid_json(self):
        response = self.client.post("/users",
                                    data=json.dumps("wrong_data"),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 422)
