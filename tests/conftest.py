import logging

import pytest
from pytest import Metafunc
from selenium import webdriver

from enum import Enum

class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    ALL = "all"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pytest_addoption(parser):
    parser.addoption(
        "--target-browser",
        action="store",
        default=Browser.CHROME.value,
        help="The target browser for the tests",
        choices=[browser.value for browser in Browser],
    )


def pytest_generate_tests(metafunc: Metafunc):
    target_browser_option = Browser(metafunc.config.getoption("--target-browser")) 
    match target_browser_option:
        case Browser.CHROME:
            supported_browsers = ["chrome"]
        case Browser.FIREFOX:
            supported_browsers = ["firefox"]
        case Browser.ALL:
            supported_browsers = ["chrome", "firefox"]
        case _:
            raise ValueError(f"Unsupported browser: {target_browser_option}")
    logger.info(f"Running tests on {supported_browsers}")
    metafunc.parametrize("target_browser", supported_browsers)


@pytest.fixture(scope="session")
def driver_factory():
    def _make_driver(browser) -> webdriver:
        match browser:
            case Browser.CHROME.value:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(options=chrome_options)
                return driver
            case Browser.FIREFOX.value:
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument("--headless")
                return webdriver.Firefox(options=firefox_options)
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    yield _make_driver
