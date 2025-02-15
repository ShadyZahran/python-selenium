import json
import logging
from http import HTTPStatus
from typing import Callable, Optional, Union

import requests

logger = logging.getLogger(__name__)


class PracticeBackendAPI:
    def __init__(self) -> None:
        self.base_url = "https://api.practicesoftwaretesting.com"
        self.user_controller = self.UserController(self)

    def make_request(
        self,
        method: Callable[..., requests.Response],
        url: str,
        params: Optional[dict[str, Union[int, str]]] = None,
        data: Optional[dict[str, str]] = None,
        auth: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        response: requests.Response = method(
            f"{self.base_url}{url}",
            params=params,
            data=json.dumps(data),
            auth=auth,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        logger.info(
            f"[{response.status_code}] {method.__name__.upper()} {response.url}"
        )
        logger.info(f"Response text: {response.text}")

        return response

    class UserController:  # Schema User
        def __init__(self, api: "PracticeBackendAPI"):
            self.api = api
            self.endpoint = "/users"

        def _post_login(self, email: str, password: str) -> requests.Response:
            payload: dict[str, str] = {"email": email, "password": password}
            response: requests.Response = self.api.make_request(
                requests.post, f"{self.endpoint}/login", data=payload
            )

            return response

        def login(self, email: str, password: str) -> requests.Response:
            response = self._post_login(email, password)
            if response.status_code in [HTTPStatus.OK, HTTPStatus.UNAUTHORIZED]:
                return response
            else:
                raise Exception(response.status_code, response.reason)
