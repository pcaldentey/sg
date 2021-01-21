import json

from http import HTTPStatus

from tests.base import BaseApiTestCase


class AlbumsEndpointTestCase(BaseApiTestCase):
    def test_default_params(self):
        path = 'http://localhost/albums'

        token = self._get_access_token('http://localhost/auth', 'testuser2', 'abcxyz')
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
            params={'page': 1, 'size': 2},
            headers={'Authorization': 'JWT {}'.format(token)}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"data": [
                {
                    "album": "For Those About To Rock We Salute You",
                    "tracks": [
                        "For Those About To Rock (We Salute You)",
                        "Put The Finger On You",
                        "Let's Get It Up",
                        "Inject The Venom",
                        "Snowballed",
                        "Evil Walks",
                        "C.O.D.",
                        "Breaking The Rules",
                        "Night Of The Long Knives",
                        "Spellbound"
                    ]
                },
                {
                    "album": "Balls to the Wall",
                    "tracks": [
                        "Balls to the Wall"
                    ]
                }],
                "meta": {"page": 1, "size": 2}
             }
        )

    def test_method_not_allowed_error(self):
        path = 'http://localhost/albums'
        response = self.request_post(
            path=path,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            params={'page': 2, 'size': 4}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 405, "description": "The method is not allowed for the requested URL.",
             "name": "Method Not Allowed"}
        )

    def test_not_auth__token_error(self):
        path = 'http://localhost/albums'

        response = self.request_get(
            path=path,
            status=HTTPStatus.UNAUTHORIZED,
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 401, "description": "Request does not contain an access token",
                "error": "Authorization Required"}
        )

    def test_expired_token_error(self):
        path = 'http://localhost/albums'
        token = (
                "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTExODU1NzUsImlhdCI6M"
                "TYxMTE4NTI3NSwibmJmIjoxNjExMTg1Mjc1LCJpZGVudGl0eSI6Mn0.rUZw9j94TZ-RpH73F_uHLQhBuKozFnl5mFXNZFJKLrk")

        response = self.request_get(
            path=path,
            status=HTTPStatus.UNAUTHORIZED,
            headers={'Authorization': 'JWT {}'.format(token)}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 401, "description": "Signature has expired", "error": "Invalid token"}
        )
