import jwt
from http_proxy.jwt_composer import _encription_algorithm, _encryption_key
from http_proxy.request_factory import _jwt_header_key
from main_server.models import DecodedJWT


def validate_header(request_headers):
    return _jwt_header_key in request_headers


def decode_jwt_content(request_headers):
    return jwt.decode(request_headers[_jwt_header_key], _encryption_key, algorithm=_encription_algorithm)


def create_decoded_jwt(request_headers):
    decoded_jwt = decode_jwt_content(request_headers)

    return DecodedJWT.objects.create(iat=decoded_jwt['iat'],
                                     jti=decoded_jwt['jti'],
                                     payload=decoded_jwt['payload'])


def store_jwt(request_headers):
    if validate_header(request_headers):
        if create_decoded_jwt(request_headers):
            return True

    return False
