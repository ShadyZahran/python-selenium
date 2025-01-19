import logging
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Callable, Optional, Union
from urllib import parse
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


class AccountType(Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    LOAN = "LOAN"


@dataclass
class Account:
    id: int
    customerId: int
    type: AccountType
    balance: float  # note: represented as 'number' in schema


class BackendAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.misc_controller = self.MiscController(self)
        self.customers_controller = self.CustomersController(self)
        self.accounts_controller = self.AccountsController(self)

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

    class CustomersController:  # Schema Customers
        def __init__(self, api: "BackendAPI"):
            self.api = api
            self.endpoint = "/customers"

        def _get_customer_acounts_by_id(self, customer_id: int) -> requests.Response:
            response: requests.Response = self.api.make_request(
                requests.get,
                f"{self.endpoint}/{customer_id}/accounts",
            )

            return response

        def get_customer_accounts(self, customer_id: int) -> list[Account]:
            response = self._get_customer_acounts_by_id(customer_id)
            if response.status_code == HTTPStatus.OK:
                accounts_list: list[Account] = [
                    Account(**account) for account in response.json()
                ]
                return accounts_list
            else:
                raise Exception(response.status_code, response.reason)

    class AccountsController:  # Schema Accounts
        def __init__(self, api: "BackendAPI"):
            self.api = api
            self.endpoint = "/accounts"

        def _get_acount_by_id(self, account_id: int) -> requests.Response:
            response: requests.Response = self.api.make_request(
                requests.get,
                f"{self.endpoint}/{account_id}",
            )

            return response

        def get_account(self, account_id: int) -> Account:
            response = self._get_acount_by_id(account_id)
            if response.status_code == HTTPStatus.OK:
                return Account(**response.json())
            else:
                raise Exception(response.status_code, response.reason)

        def _post_deposit_to_account(
            self, account_id: int, amount: float
        ) -> requests.Response:
            params = {
                "accountId": account_id,
                "amount": amount
            }
            response: requests.Response = self.api.make_request(
                requests.post,
                f"/deposit?{parse.urlencode(params)}",
            )

            return response

        def deposit_to_account(
            self, account_id: int, amount: float
        ) -> requests.Response:
            response = self._post_deposit_to_account(account_id, amount)
            if response.status_code == HTTPStatus.OK:
                return response
            else:
                raise Exception(response.status_code, response.reason)
