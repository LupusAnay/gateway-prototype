import json

from unittest import skip
from flask import current_app

from auth.tests.base_test_case import BaseTestCase
from auth.tests.api_methods import register_user, login, logout


class TestSession(BaseTestCase):
    def setUp(self):
        super().setUp()
        response = register_user(self, 'user', 'pass', 'user@mail.com')
        data = json.loads(response.data.decode())
        self.token = data.get('jwt')

    def test_login(self):
        response = login(self, 'user', 'pass')
        current_app.logger.info(response)
        self.assert200(response)

        data = json.loads(response.data.decode())

        self.assertEqual(self.token, data.get('jwt'))

    def test_login_with_wrong_data(self):
        response_wrong_both = login(self, 'wrong_user', 'wrong_pass')
        response_wrong_pass = login(self, 'user', 'wrong_pass')
        response_wrong_user = login(self, 'wrong_user', 'pass')

        self.assert404(response_wrong_both)
        self.assert404(response_wrong_pass)
        self.assert404(response_wrong_user)

    @skip('Not implemented')
    def test_logout(self):
        response = logout(self, self.token)

        self.assertEqual(response.status_code, 204)
