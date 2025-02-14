import logging
from http import HTTPStatus

import allure
import pytest

from interfaces.practice_backend_api import PracticeBackendAPI

logger = logging.getLogger(__name__)


@allure.feature("Login")
@allure.story("API: Login with valid credentials")
@pytest.mark.parametrize(
    "email, password", [("customer@practicesoftwaretesting.com", "welcome01")]
)
def test_customer_login_valid_credentials(
    email: str, password: str, practice_backend_api: PracticeBackendAPI
) -> None:
    """Test user login endpoint returns bearer access token using valid customer credentials"""

    response = practice_backend_api.user_controller.login(email, password)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


@allure.feature("Login")
@allure.story("API: Login with valid credentials")
@pytest.mark.parametrize(
    "email, password", [("customer@practicesoftwaretesting.com", "welcome01")]
)
def test_customer_login_valid_response(
    email: str, password: str, practice_backend_api: PracticeBackendAPI
) -> None:
    """Test user login endpoint has valid response using valid customer credentials"""

    expected_keys = ["access_token", "token_type", "expires_in"]

    response = practice_backend_api.user_controller.login(email, password)
    missing_keys = [key for key in expected_keys if key not in response.json()]

    assert response.status_code == HTTPStatus.OK
    assert not missing_keys, f"{missing_keys} not found in response"
