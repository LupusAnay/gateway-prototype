import json

from .base_test_case import BaseTestCase


def register_user(self, username, password, first_name, second_name):
    response = self.app.post("/register",
                             data=json.dumps(dict(username=username,
                                                  password=password,
                                                  first_name=first_name,
                                                  second_name=second_name)
                                             ),
                             content_type='application/json')
    return json.loads(response.data.decode())


class TestCreateUser(BaseTestCase):
    def test_registration(self):
        data = register_user(self,
                             'new_user',
                             'new_user_password',
                             'new',
                             'user')
        self.assertTrue(data['access_token'] != 0)
        self.assertTrue(data['refresh_token'] != 0)

    def test_registration_with_already_registered_user(self):
        data = register_user(self,
                             TestingUser.USER,
                             TestingUser.PASSWORD,
                             TestingUser.FIRST_NAME,
                             TestingUser.SECOND_NAME)
        self.assertTrue(data['error'] == 'User with this username is already '
                                         'registered')
