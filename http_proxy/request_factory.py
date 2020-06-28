import requests
import json

from django.conf import settings
from http_proxy.jwt_composer import compose_jwt


_request_timeout = 10
_post = 'post'
_jwt_header_key = 'x-my-jwt'
_destination_keyword = 'Destination'


def validate_payload(payload):
    """
    Verifies if the payload is JSON compatible.
    """
    try:
        json.loads(payload)
    except TypeError:
        return False
    return True


def decode_request_body(request_body):
    """
    Returns the decoded request body if the content is compatible with the JWT.
    """
    return request_body.decode() if validate_payload(request_body.decode()) else ""


def compose_destination(headers):
    """
    Defines if the request should be sent to the default server URL
    or for a destination set by the original request.
    """
    if _destination_keyword in headers:
        return headers[_destination_keyword]
    return settings.MAIN_SERVER_URL


def initialize_header_with_jwt(request):
    """
    Initializes the new request headers with the JWT
    """
    return {_jwt_header_key: compose_jwt(decode_request_body(request.body))}


def compose_header(request_content):
    """
    Compose the new headers with both the original headers and the JWT.
    """
    headers = initialize_header_with_jwt(request_content)

    if request_content.headers:
        headers.update(request_content.headers)

    return headers


def generate_request(request_content):
    """
    Execute the POST requests with:
        - Either the default destination or a destination defined by the original request
        - Original headers and the Encoded JWT
    """
    return requests.request(_post,
                            compose_destination(request_content.headers),
                            headers=compose_header(request_content),
                            data=request_content.body.decode())
