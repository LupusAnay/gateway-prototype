from flask import Response
import json


def register_user(self, username, password, email) -> Response:
    return self.client.post("/users",
                            data=json.dumps(dict(username=username,
                                                 password=password,
                                                 email=email)),
                            content_type='application/json')


def login(self, username, password) -> Response:
    return self.client.post('/session',
                            data=json.dumps(dict(username=username,
                                                 password=password)
                                            ),
                            content_type='application/json')


def logout(self, token) -> Response:
    return self.client.delete('/session',
                              headers=dict(authorization=f'Bearer {token}')
                              )


def delete_user(self, token, username) -> Response:
    return self.client.delete(f'/users/{username}',
                              headers=dict(authorization=f'Bearer {token}'))


def get_user_info(self, token, username):
    return self.client.get(f'/users/{username}',
                           headers=dict(authorization=f'Bearer {token}'))

