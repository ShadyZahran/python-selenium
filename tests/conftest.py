import logging
import subprocess
from enum import Enum

import allure
import pytest
from pytest import Metafunc
from selenium import webdriver


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
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
        case Browser.EDGE:
            supported_browsers = ["edge"]
        case Browser.ALL:
            supported_browsers = ["chrome", "firefox", "edge"]
        case _:
            raise ValueError(f"Unsupported browser: {target_browser_option}")
    logger.info(f"Running tests on {supported_browsers}")
    metafunc.parametrize("target_driver", supported_browsers, indirect=True)


@pytest.fixture(scope="session")
def driver_factory():
    def _make_driver(browser) -> webdriver:
        match browser:
            case Browser.CHROME.value:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
                chrome_options.add_argument("--headless")
                chrome_service = webdriver.ChromeService(
                    log_output=subprocess.STDOUT, service_args=["--log-level=DEBUG"]
                )
                driver = webdriver.Chrome(
                    service=chrome_service, options=chrome_options
                )
                return driver
            case Browser.FIREFOX.value:
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument("--headless")
                firefox_service = webdriver.FirefoxService(
                    log_output=subprocess.STDOUT, service_args=["--log", "debug"]
                )
                return webdriver.Firefox(
                    service=firefox_service, options=firefox_options
                )
            case Browser.EDGE.value:
                edge_options = webdriver.EdgeOptions()
                edge_options.add_argument("--headless")
                edge_service = webdriver.EdgeService(
                    log_output=subprocess.STDOUT, service_args=["--log-level=DEBUG"]
                )
                return webdriver.Edge(service=edge_service, options=edge_options)
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    yield _make_driver


@pytest.fixture(scope="function")
def target_driver(request, driver_factory):
    target_driver_value: str = request.param
    driver: webdriver = driver_factory(target_driver_value)
    yield driver
    Attach_screenshot(driver, f"test_{request.node.name}")
    driver.quit()


@allure.step("Attaching screenshot")
def Attach_screenshot(driver: webdriver, name: str):
    screenshot = driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
