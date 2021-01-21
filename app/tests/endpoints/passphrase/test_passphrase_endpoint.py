import json

from http import HTTPStatus

from tests.base import BaseApiTestCase


class PassphraseEndpointTestCase(BaseApiTestCase):
    def test_basic(self):
        path = 'http://localhost/passphrase/basic'

        pp_list = [
                     'aa bb cc dd ee',
                     'aa bb cc dd aa',
                     'aa bb cc dd aaa'
                    ]
        response = self.request_post(
            path=path,
            status=HTTPStatus.OK,
            body={
                'passphrase': '\n'.join(pp_list),
            }
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'total passphrases': 3, 'valid passphrases': 2}
        )

    def test_advanced(self):
        path = 'http://localhost/passphrase/advanced'

        pp_list = [
                    'abcde fghij',
                    'abcde xyz ecdab',
                    'a ab abc abd abf abj',
                    'iiii oiii ooii oooi oooo',
                    'oiii ioii iioi iiio',
                    ]
        response = self.request_post(
            path=path,
            status=HTTPStatus.OK,
            body={
                'passphrase': '\n'.join(pp_list),
            }
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'total passphrases': 5, 'valid passphrases': 3}
        )

    def test_basic_no_body_error(self):
        path = 'http://localhost/passphrase/basic'

        response = self.request_post(
            path=path,
            status=HTTPStatus.BAD_REQUEST,
            body={}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 400, "description": "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)",
                "name": "Bad Request"}
        )

    def test_basic_empty_passphrase(self):
        path = 'http://localhost/passphrase/basic'

        response = self.request_post(
            path=path,
            status=HTTPStatus.BAD_REQUEST,
            body={'passphrase': ''}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'status_code': 400,
             'description': 'passphrase parameter invalid.',
             'name': 'Bad Request'}
        )

    def test_basic_breakline_passphrase(self):
        path = 'http://localhost/passphrase/basic'

        response = self.request_post(
            path=path,
            status=HTTPStatus.OK,
            body={'passphrase': '\n'}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'total passphrases': 2, 'valid passphrases': 0}
        )

    def test_advanced_no_body_error(self):
        path = 'http://localhost/passphrase/advanced'

        response = self.request_post(
            path=path,
            status=HTTPStatus.BAD_REQUEST,
            body={}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {"status_code": 400, "description": "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)",
                "name": "Bad Request"}
        )

    def test_advanced_empty_passphrase(self):
        path = 'http://localhost/passphrase/advanced'

        response = self.request_post(
            path=path,
            status=HTTPStatus.BAD_REQUEST,
            body={'passphrase': ''}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'status_code': 400,
             'description': 'passphrase parameter invalid.',
             'name': 'Bad Request'}
        )

    def test_advanced_breakline_passphrase(self):
        path = 'http://localhost/passphrase/advanced'

        response = self.request_post(
            path=path,
            status=HTTPStatus.OK,
            body={'passphrase': '\n'}
        )
        self.assertDictEqual(
            json.loads(response.text),
            {'total passphrases': 2, 'valid passphrases': 0}
        )
