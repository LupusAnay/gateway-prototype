import json

from auth.tests.base_test_case import BaseTestCase
from auth.tests.api_methods import update_user, register_user


class TestUpdateUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        register_user(self, 'wrong_user', 'pass', 'mail@mail.com')
        response = register_user(self, 'user', 'pass', 'user@mail.com')
        data = json.loads(response.data.decode())
        self.token = data.get('jwt')

    def test_update_user(self):
        new_info = dict(email='new@mail.com',
                        username='new_user',
                        password='new_pass')
        response = update_user(self, self.token, 'user', new_info)

        self.assertEqual(response.status_code, 204)

    def test_update_user_without_rights(self):
        new_info = dict(email='new@mail.com',
                        username='new_user',
                        password='new_pass')
        response_wrong_token = update_user(self, 'wrong_token', 'user',
                                           new_info)
        response_wrong_user = update_user(self, self.token, 'wrong_user',
                                          new_info)

        self.assertEqual(response_wrong_user.status_code, 403)
        self.assertEqual(response_wrong_token.status_code, 403)

    def test_update_without_data(self):
        new_info = None
        response = update_user(self, self.token, 'user', new_info)

        self.assertEqual(response.status_code, 422)
