import jwt


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, 'key', algorithm='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
