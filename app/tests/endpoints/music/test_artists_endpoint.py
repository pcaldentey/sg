import json

from http import HTTPStatus

from tests.base import BaseApiTestCase


class ArtistsEndpointTestCase(BaseApiTestCase):
    def test_default_params(self):
        path = 'http://localhost/artists'
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'data': [
                {'id': 1, 'name': 'AC/DC'}, {'id': 2, 'name': 'Accept'}, {'id': 3, 'name': 'Aerosmith'},
                {'id': 4, 'name': 'Alanis Morissette'}, {'id': 5, 'name': 'Alice In Chains'},
                {'id': 6, 'name': 'Antônio Carlos Jobim'}, {'id': 7, 'name': 'Apocalyptica'},
                {'id': 8, 'name': 'Audioslave'}, {'id': 9, 'name': 'BackBeat'}, {'id': 10, 'name': 'Billy Cobham'},
                {'id': 11, 'name': 'Black Label Society'}, {'id': 12, 'name': 'Black Sabbath'},
                {'id': 13, 'name': 'Body Count'}, {'id': 14, 'name': 'Bruce Dickinson'},
                {'id': 15, 'name': 'Buddy Guy'}, {'id': 16, 'name': 'Caetano Veloso'},
                {'id': 17, 'name': 'Chico Buarque'}, {'id': 18, 'name': 'Chico Science & Nação Zumbi'},
                {'id': 19, 'name': 'Cidade Negra'}, {'id': 20, 'name': 'Cláudio Zoli'}
                ]
             }
        )

    def test_pagination_params(self):
        path = 'http://localhost/artists'
        response = self.request_get(
            path=path,
            status=HTTPStatus.OK,
            params={'page': 2, 'size': 4}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'data': [
                {'id': 5, 'name': 'Alice In Chains'},
                {'id': 6, 'name': 'Antônio Carlos Jobim'},
                {'id': 7, 'name': 'Apocalyptica'},
                {'id': 8, 'name': 'Audioslave'}
                ]
             }
        )

    def test_method_not_allowed_error(self):
        path = 'http://localhost/artists'
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
