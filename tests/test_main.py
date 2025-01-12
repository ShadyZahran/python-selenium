import pytest
from index_page import ParabankIndexPage




@pytest.mark.parametrize("username, password", [("john", "invalid")])
def test_login_invalid_credentials(
    username,
    password,
    driver_factory,
    target_browser,
):
    created_driver = driver_factory(target_browser)

    index_page = ParabankIndexPage(created_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    assert index_page.login_section.is_error_message_invalid_credentials()

    created_driver.quit()

@pytest.mark.parametrize("username, password", [("", "")])
def test_login_empty_fields(
    username,
    password,
    driver_factory,
    target_browser,
):
    created_driver = driver_factory(target_browser)

    index_page = ParabankIndexPage(created_driver)
    index_page.load()
    index_page.login_section.login(username, password)

    assert index_page.login_section.is_error_message_empty_fields()

    created_driver.quit()