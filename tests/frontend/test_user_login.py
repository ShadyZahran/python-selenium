import logging

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@allure.feature("Login")
@allure.story("E2E: Login with valid credentials")
@pytest.mark.parametrize(
    "email, password, fullname",
    [("customer@practicesoftwaretesting.com", "welcome01", "Jane Doe")],
)
def test_customer_login_valid_credentials(
    email: str, password: str, fullname: str, target_driver: WebDriver
) -> None:
    """Test login functionality using valid customer credentials"""
    login_page = LoginPage(target_driver)
    login_page.load()
    login_page.login(email, password)
    login_page.wait_for_login_redirection()

    displayed_name: str = login_page.nav_bar.get_signed_in_username()
    assert displayed_name == fullname
