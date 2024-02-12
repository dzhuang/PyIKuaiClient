import base64
import hashlib
import json
from urllib.parse import urljoin

import requests

from .constants import (JSON_RESPONSE_ERRMSG, JSON_RESPONSE_RESULT,
                        json_result_code)
from .exceptions import AuthenticationError, RequestError


class IKuai:  # noqa
    def __init__(self, url, username, password):
        self._username = username
        self._passwd = password
        self.base_url = url.strip().rstrip("/")
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = requests.session()
            self.authenticate()

        return self._session

    def authenticate(self):
        passwd = hashlib.md5(self._passwd.encode()).hexdigest()
        pass_encoded = base64.b64encode(f'salt_11{passwd}'.encode()).decode()
        login_info = {
            'passwd': passwd,
            'pass': pass_encoded,
            'remember_password': "",
            'username': self._username
        }
        if self._session is None:
            self._session = requests.session()

        response = (
            self._session.post(f'{self.base_url}/Action/login', json=login_info))
        if response.status_code != 200:
            self._session = None
            raise AuthenticationError(
                f"Failed to authenticate with status code {response.status_code}")

        content = response.json()
        if content[JSON_RESPONSE_RESULT] != json_result_code.code_10000:
            self._session = None
            raise AuthenticationError(
                "Failed to authenticate with result code "
                f"{content[JSON_RESPONSE_RESULT]}: {content[JSON_RESPONSE_ERRMSG]}."
            )

    def exec(self, func, action, param):
        payload = {
            "func_name": func,
            "action": action,
            "param": param
        }
        response = self.session.post(
            urljoin(self.base_url, "/Action/call"), json=payload)
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                raise RequestError(
                    f"Error parsing response: {response.content.decode()}")

        raise RequestError(
            f"Request failed with response status code: {response.status_code}")
