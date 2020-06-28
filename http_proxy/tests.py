import jwt
from datetime import timedelta
from django.conf import settings
from django.test import TestCase, RequestFactory, Client
from http_proxy.apps import HttpProxyConfig
from http_proxy.models import ProxyStatus
from http_proxy.controller import (
    current_number_of_requests,
    update_proxy_status,
    select_status_object)
from http_proxy.request_factory import (
    generate_request,
    _jwt_header_key,
    validate_payload,
    compose_destination,
    compose_header)
from http_proxy.jwt_composer import (
    compose_jwt_content,
    compose_jwt,
    _encryption_key,
    _encription_algorithm)


_test_payload = {"user": "username", "date": "todays date"}
_claim_keys = ['iat', 'jti', 'payload']
_reqres_users_api = "http://reqres.in/api/users/"
_invalid_json = None


class ProxyTestCase(TestCase):

    def setup_status_object(self):
        return ProxyStatus.objects.create(id=1)

    def verify_jwt_content(self, content):
        for claim in _claim_keys:
            assert claim in content

        assert content['payload'] == _test_payload

    def compose_test_request(self):
        factory = RequestFactory()
        return factory.post('/proxy/',
                            _test_payload,
                            content_type='application/json',
                            HTTP_destination=_reqres_users_api)

    def test_claims_format_and_content(self):
        jwt_content = compose_jwt_content(_test_payload)

        self.verify_jwt_content(jwt_content)

    def test_jwt_composition_and_encoding(self):

        decoded_jwt = jwt.decode(compose_jwt(_test_payload),
                                 _encryption_key,
                                 algorithm=_encription_algorithm)

        self.verify_jwt_content(decoded_jwt)

    def test_request_generation(self):
        assert generate_request(self.compose_test_request()).status_code == 200

    def test_request_headers(self):

        header = compose_header(self.compose_test_request())
        assert _jwt_header_key in header

    def test_proxy_api_and_request_count(self):
        self.setup_status_object()

        client = Client()
        response = client.post('/proxy/',
                               _test_payload,
                               content_type='application/json',
                               HTTP_destination=_reqres_users_api)

        assert response.status_code == 200
        assert current_number_of_requests() == 1

    def test_request_count_increment_and_time_from_start(self):
        self.setup_status_object()
        assert select_status_object().time_from_start() < timedelta(seconds=30)
        assert current_number_of_requests() == 0

        update_proxy_status()

        assert current_number_of_requests() == 1

    def test_proxy_status_string(self):
        proxy_status = self.setup_status_object()
        status_string = f"Start Time: { proxy_status.start_time }, { proxy_status.request_count } requests received"
        assert str(proxy_status) == status_string

    def test_destination_and_validation(self):

        assert settings.MAIN_SERVER_URL == compose_destination({"content_type": "application/json"})
        assert not validate_payload(_invalid_json)

    def test_status_page(self):
        client = Client()
        status_page = client.get('/')

        assert status_page.status_code == 200

    def test_app_name(self):
        self.assertEqual(HttpProxyConfig.name, 'HTTP Proxy')
