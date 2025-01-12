import allure
import pytest
from index_page import ParabankIndexPage


@allure.feature("Login")
@allure.story("Login with invalid credentials")
@pytest.mark.parametrize("username, password", [("john", "invalid")])
def test_login_invalid_credentials(
    username,
    password,
    target_driver,
):
    index_page = ParabankIndexPage(target_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    assert index_page.login_section.is_error_message_invalid_credentials()


@allure.feature("Login")
@allure.story("Login with empty fields")
@pytest.mark.parametrize("username, password", [("", "")])
def test_login_empty_fields(
    username,
    password,
    target_driver,
):
    index_page = ParabankIndexPage(target_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    assert index_page.login_section.is_error_message_empty_fields()
