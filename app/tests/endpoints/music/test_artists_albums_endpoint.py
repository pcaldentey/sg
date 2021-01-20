import json

from http import HTTPStatus

from tests.base import BaseApiTestCase


class ArtistsAlbumsEndpointTestCase(BaseApiTestCase):
    def test_default_params(self):
        path = 'http://localhost/artists/{}/albums'.format(1)  # AC/DC
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
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
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
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
        response = self.request_get(
            path=path,
            status=HTTPStatus.NOT_FOUND,
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"code": 404, "description": "Artist not found.", "name": "Not Found"}
        )

    def test_method_not_allowed_error(self):
        path = 'http://localhost/artists/{}/albums'.format(1)  # AC/DC
        response = self.request_post(
            path=path,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"code": 405, "description": "The method is not allowed for the requested URL.",
             "name": "Method Not Allowed"}
        )
