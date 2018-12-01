import json

from jsonschema import validate
from auth.tests.base_test_case import BaseTestCase
from auth.tests.api_methods import get_user_info, register_user, delete_user

info_schema = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string'},
        'user_info': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email'},
                'id': {'type': 'integer'},
                'registered_on': {
                    'type': 'string',
                    'format': 'datetime'
                },
                'role': {'type': 'string'},
                'username': {'type': 'string'}
            },
            'required': ['email', 'id', 'registered_on', 'role', 'username']
        }
    },
    'required': ['status', 'user_info']
}


class TestGetUserInfo(BaseTestCase):
    def setUp(self):
        super().setUp()
        register_user(self, 'wrong_user', 'pass', 'mail@mail.com')
        response = register_user(self, 'user', 'pass', 'user@mail.com')
        data = json.loads(response.data.decode())
        self.token = data.get('jwt')

    def test_get_user_info(self):
        response = get_user_info(self, self.token, 'user')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        validate(data, info_schema)

    def test_get_user_info_without_rights(self):
        response_wrong_user = get_user_info(self, self.token, 'wrong_user')
        response_wrong_token = get_user_info(self, 'wrong_token', 'user')

        self.assertEqual(response_wrong_user.status_code, 403)
        self.assertEqual(response_wrong_token.status_code, 403)

    def test_get_info_without_user(self):
        delete_user(self, self.token, 'user')
        response = get_user_info(self, self.token, 'user')

        self.assert404(response)
