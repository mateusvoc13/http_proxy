from django.test import TestCase, Client

from http_proxy.tests import _test_payload
from http_proxy.jwt_composer import compose_jwt

from main_server.apps import MainServerConfig
from main_server.models import DecodedJWT


class JWTTestCase(TestCase):

    def mock_request_with_jwt(self):
        factory = Client()
        return factory.post('/server/',
                            _test_payload,
                            content_type='application/json',
                            HTTP_x_my_jwt=compose_jwt(_test_payload))

    def test_jwt_creation(self):
        self.mock_request_with_jwt()
        decoded_jwt = DecodedJWT.objects.get(id=1)
        assert str(decoded_jwt)

    def test_post_without_jwt(self):
        factory = Client()
        factory.post('/server/',
                     _test_payload,
                     content_type='application/json')

        assert not DecodedJWT.objects.filter(id=1).first()

    def test_app_name(self):
        self.assertEqual(MainServerConfig.name, 'Main Server')
