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
def test_user_login(
    email: str, password: str, practice_backend_api: PracticeBackendAPI
) -> None:
    response = practice_backend_api.user_controller.login(email, password)
    assert response.status_code == HTTPStatus.OK
