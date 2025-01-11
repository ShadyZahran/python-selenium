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
    index_page.login(username, password)

    assert index_page.is_error_title_located()

    created_driver.quit()
