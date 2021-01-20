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
                }]
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
            {"code": 405, "description": "The method is not allowed for the requested URL.",
             "name": "Method Not Allowed"}
        )
