import jwt
import json
import hashlib

from datetime import datetime
from django.conf import settings
from http_proxy.controller import current_number_of_requests


_encription_algorithm = 'HS512'
_encryption_key = settings.JWT_KEY
_iat = 'iat'
_jti = 'jti'
_payload = 'payload'


def compose_nonce():

    nonce_content = {
        'request_number': current_number_of_requests(),
        'time_now': datetime.utcnow().strftime('%B %d %Y, %H:%M:%S'),
    }

    return hashlib.md5(json.dumps(nonce_content).encode("utf-8")).hexdigest()


def compose_jwt_content(payload):
    """
    Returns the content for the JWT
    """
    return {
        _iat: datetime.utcnow(),
        _jti: compose_nonce(),
        _payload: payload
    }


def compose_jwt(payload):
    """
    Generates the encoded JWT
    """
    return jwt.encode(compose_jwt_content(payload),
                      _encryption_key,
                      algorithm=_encription_algorithm)
