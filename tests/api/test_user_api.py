import logging
from http import HTTPStatus

import allure
import pytest
from conftest import get_valid_customer
from pytest import MonkeyPatch
from requests import Response

from interfaces.parabank_backend_api import (
    Account,
    BackendAPI,
    CustomerProfile,
)

logger = logging.getLogger(__name__)


@allure.feature("Login")
@allure.story("API: Login with valid credentials")
@pytest.mark.parametrize("customer_profile", get_valid_customer())
def test_get_login_valid_credentials(
    customer_profile: CustomerProfile, backend_api: BackendAPI
) -> None:
    response_customer = backend_api.misc_controller.get_login(
        customer_profile.credentials
    )
    assert response_customer.id == customer_profile.data.id


def test_get_customer_accounts(backend_api: BackendAPI) -> None:
    customer_id: int = 12212
    customer_accounts_list: list[Account] = (
        backend_api.customers_controller.get_customer_accounts(customer_id)
    )
    for customer_account in customer_accounts_list:
        logger.info(customer_account)

    account: Account = backend_api.accounts_controller.get_account(12345)
    logger.info(f"account: {account}")


def test_deposit_money_to_account(
    backend_api: BackendAPI, monkeypatch: MonkeyPatch
) -> None:
    def mock_deposit_response(account_id: int, deposit_amount: float) -> Response:
        response = Response()
        response.status_code = 200
        response._content = (
            f"Successfully deposited ${deposit_amount} to account #{account_id}!"
        ).encode("utf-8")
        response.encoding = "utf-8"
        return response

    monkeypatch.setattr(
        backend_api.accounts_controller, "deposit_to_account", mock_deposit_response
    )
    account_id: int = 13344
    deposit_amount: float = 100.00
    response = backend_api.accounts_controller.deposit_to_account(
        account_id, deposit_amount
    )
    logger.info(response.text)

    assert response.status_code == HTTPStatus.OK
