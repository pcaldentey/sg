import json

from http import HTTPStatus

from tests.base import BaseApiTestCase


class ArtistsAlbumsEndpointTestCase(BaseApiTestCase):
    def test_default_params(self):
        path = 'http://localhost/artists/{}/albums'.format(1)  # AC/DC

        token = self._get_access_token('http://localhost/auth', 'testuser2', 'abcxyz')
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
            headers={'Authorization': 'JWT {}'.format(token)}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {
                "albums": [
                    "For Those About To Rock We Salute You",
                    "Let There Be Rock"
                ],
                "artist name": "AC/DC"
            }
        )

    def test_artist_no_albums(self):
        path = 'http://localhost/artists/{}/albums'.format(45)

        token = self._get_access_token('http://localhost/auth', 'testuser2', 'abcxyz')
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
            headers={'Authorization': 'JWT {}'.format(token)}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {
                "albums": [],
                "artist name": "Sandra De Sá"
            }
        )

    def test_artist_non_existing(self):
        path = 'http://localhost/artists/{}/albums'.format(4500)

        token = self._get_access_token('http://localhost/auth', 'testuser2', 'abcxyz')
        response = self.request_get(
            path=path,
            status=HTTPStatus.NOT_FOUND,
            headers={'Authorization': 'JWT {}'.format(token)}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 404, "description": "Artist not found.", "name": "Not Found"}
        )

    def test_not_auth__token_error(self):
        path = 'http://localhost/artists/{}/albums'.format(1)  # AC/DC

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
        path = 'http://localhost/artists/{}/albums'.format(4500)
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

    def test_method_not_allowed_error(self):
        path = 'http://localhost/artists/{}/albums'.format(1)  # AC/DC
        response = self.request_post(
            path=path,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 405, "description": "The method is not allowed for the requested URL.",
             "name": "Method Not Allowed"}
        )
