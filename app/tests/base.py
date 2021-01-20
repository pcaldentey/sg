import json
import requests

from http import HTTPStatus
from urllib.parse import urlencode

from unittest import TestCase


class BaseApiTestCase(TestCase):
    """Prepare helpers to simulate API requests."""

    def setUp(self):
        super().setUp()

        self.request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        self.request_methods = {
            'DELETE': requests.delete,
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'PATCH': requests.patch,
        }

    def _request_method(self, method_name, path, status, headers, body=None, params=None):
        if headers:
            self.request_headers.update(headers)

        request_method = self.request_methods[method_name]

        request_body = json.dumps(body, ensure_ascii=False) if body else None
        request_params = urlencode(params, safe=',') if params else None

        response = request_method(
            path,
            data=request_body,
            headers=self.request_headers,
            params=request_params,
        )
        self.assertEqual(response.status_code, status, response.content)

        return response

    def request_get(self, path, params=None, status=HTTPStatus.OK, headers=None):
        return self._request_method('GET', path, status, headers, params=params)

    def request_post(self, path, body=None, params=None, status=HTTPStatus.OK, headers=None):
        return self._request_method('POST', path, status, headers, body, params)

    def request_patch(self, path, body=None, status=HTTPStatus.OK, headers=None):
        return self._request_method('PATCH', path, status, headers, body)

    def request_delete(self, path, status=HTTPStatus.OK, headers=None):
        return self._request_method('DELETE', path, status, headers)

    def request_put(self, path, body, status=HTTPStatus.OK, headers=None):
        return self._request_method('PUT', path, status, headers, body)

    def _get_access_token(self, path, user, password):
        response = self.request_post(
            path=path,
            status=HTTPStatus.OK,
            body={
                "username": user,
                "password": password
            }
        )
        data = json.loads(response.text)
        return data['access_token']
