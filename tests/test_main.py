import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.index_page import ParabankIndexPage


@allure.feature("Login")
@allure.story("Login with invalid credentials")
@pytest.mark.parametrize("username, password", [("john", "invalid")])
def test_login_invalid_credentials(
    username: str,
    password: str,
    target_driver: WebDriver,
) -> None:
    index_page = ParabankIndexPage(target_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    error_message = index_page.get_text(index_page.login_section.ERROR_MESSAGE)
    assert error_message == index_page.login_section.error_message_invalid_credentials


@allure.feature("Login")
@allure.story("Login with empty fields")
@pytest.mark.parametrize("username, password", [("", "")])
def test_login_empty_fields(
    username: str,
    password: str,
    target_driver: WebDriver,
) -> None:
    index_page = ParabankIndexPage(target_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    error_message = index_page.get_text(index_page.login_section.ERROR_MESSAGE)
    assert error_message == index_page.login_section.error_message_empty_fields
