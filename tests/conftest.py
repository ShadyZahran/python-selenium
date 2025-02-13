import logging
import subprocess
from enum import Enum
from typing import Callable, Generator

import allure
import pytest
from pytest import FixtureRequest, Metafunc, Parser
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from interfaces.practice_backend_api import PracticeBackendAPI


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    ALL = "all"


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--target-browser",
        action="store",
        default=Browser.ALL.value,
        help="The target browser for the tests",
        choices=[browser.value for browser in Browser],
    )


def pytest_generate_tests(metafunc: Metafunc) -> None:
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
    if "target_driver" in metafunc.fixturenames:
        metafunc.parametrize("target_driver", supported_browsers, indirect=True)


@pytest.fixture(scope="session")
def driver_factory() -> Generator[Callable[[str], WebDriver], None, None]:
    def _make_driver(browser: str) -> WebDriver:
        match browser:
            case Browser.CHROME.value:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920,1080")
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
                firefox_options.add_argument("--width=1920")
                firefox_options.add_argument("--height=1080")
                firefox_service = webdriver.FirefoxService(
                    log_output=subprocess.STDOUT, service_args=["--log", "debug"]
                )
                return webdriver.Firefox(
                    service=firefox_service, options=firefox_options
                )
            case Browser.EDGE.value:
                edge_options = webdriver.EdgeOptions()
                edge_options.add_argument("--headless")
                edge_options.add_argument("--window-size=1920,1080")
                edge_service = webdriver.EdgeService(
                    log_output=subprocess.STDOUT, service_args=["--log-level=DEBUG"]
                )
                return webdriver.Edge(service=edge_service, options=edge_options)
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    yield _make_driver


@pytest.fixture(scope="function")
def target_driver(
    request: FixtureRequest, driver_factory: Callable[[str], WebDriver]
) -> Generator[WebDriver, None, None]:
    target_driver_value: str = request.param
    driver: WebDriver = driver_factory(target_driver_value)
    yield driver
    Attach_screenshot(driver, f"test_{request.node.name}")
    driver.quit()


@allure.step("Attaching screenshot")
def Attach_screenshot(driver: WebDriver, name: str) -> None:
    screenshot = driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="session")
def practice_backend_api() -> Generator[PracticeBackendAPI, None, None]:
    api = PracticeBackendAPI()
    yield api
