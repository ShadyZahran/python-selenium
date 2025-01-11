import logging

import pytest
from pytest import Metafunc
from selenium import webdriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pytest_addoption(parser):
    parser.addoption(
        "--target-browser",
        action="store",
        default="chrome",
        help="The target browser for the tests",
        choices=["chrome", "firefox", "all"],
    )


def pytest_generate_tests(metafunc: Metafunc):
    target_browser_option = metafunc.config.getoption("--target-browser")
    match target_browser_option:
        case "chrome":
            supported_browsers = ["chrome"]
        case "firefox":
            supported_browsers = ["firefox"]
        case "all":
            supported_browsers = ["chrome", "firefox"]
    metafunc.parametrize("target_browser", supported_browsers)


@pytest.fixture(scope="session")
def driver_factory():
    def _make_driver(browser) -> webdriver:
        match browser:
            case "chrome":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(options=chrome_options)
                return driver
            case "firefox":
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument("--headless")
                return webdriver.Firefox(options=firefox_options)
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    yield _make_driver
