import logging
from dataclasses import dataclass
from http import HTTPStatus
from typing import Callable, Optional, Union

import requests

logger = logging.getLogger(__name__)


@dataclass
class Address:  # Schema: Address
    street: str
    city: str
    state: str
    zipCode: str


@dataclass
class Customer:  # Schema: Customer
    id: int
    firstName: str
    lastName: str
    address: Address
    phoneNumber: str
    ssn: str


@dataclass
class Auth:
    username: str
    password: str


@dataclass
class CustomerProfile:
    credentials: Auth
    data: Customer


class BackendAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.misc_controller = self.MiscController(self)

    def make_request(
        self,
        method: Callable[..., requests.Response],
        url: str,
        params: Optional[dict[str, Union[int, str]]] = None,
        payload_json: Optional[dict[str, Union[int, str]]] = None,
        auth: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        response: requests.Response = method(
            f"{self.base_url}{url}",
            params=params,
            json=payload_json,
            auth=auth,
            headers={"accept": "application/json"},
        )
        logger.info(
            f"[{response.status_code}] {method.__name__.upper()} {response.url}"
        )
        logger.info(f"Response text: {response.text}")

        return response

    class MiscController:  # Schema Misc
        def __init__(self, api: "BackendAPI"):
            self.api = api
            self.endpoint = "/login"

        def _get_login(self, credentials: Auth) -> requests.Response:
            response: requests.Response = self.api.make_request(
                requests.get,
                f"{self.endpoint}/{credentials.username}/{credentials.password}",
            )

            return response

        def get_login(self, credentials: Auth) -> Customer:
            response = self._get_login(credentials)
            if response.status_code == HTTPStatus.OK:
                return Customer(**response.json())
            else:
                raise Exception(response.status_code, response.reason)
