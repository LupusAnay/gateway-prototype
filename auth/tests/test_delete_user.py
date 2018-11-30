import json

from auth.tests.base_test_case import BaseTestCase
from auth.tests.api_methods import register_user, delete_user


class TestDeleteUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        register_user(self, 'wrong_user', 'pass', 'mail@mail.com')
        response = register_user(self, 'user', 'pass', 'user@mail.com')
        data = json.loads(response.data.decode())
        self.token = data.get('jwt')

    def test_delete_user(self):
        response = delete_user(self, self.token, 'user')

        self.assertEqual(response.status_code, 204)

    def test_delete_user_without_permission(self):
        response_invalid_token = delete_user(self, 'invalid_token', 'user')
        response_invalid_user = delete_user(self, self.token, 'wrong_user')

        self.assertEqual(response_invalid_token.status_code, 403)
        self.assertEqual(response_invalid_user.status_code, 403)
