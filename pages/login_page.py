import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator

logger = logging.getLogger(__name__)


class ParabankLoginSection(BasePage):
    USERNAME_FIELD: Locator = (By.XPATH, "//input[@name='username']", 5)
    PASSWORD_FIELD: Locator = (By.XPATH, "//input[@name='password']", 5)
    LOGIN_BUTTON: Locator = (By.XPATH, "//input[@value='Log In']", 5)

    GREETING_MESSAGE: Locator = (By.XPATH, "//p[@class='smallText']", 5)
    ERROR_TITLE: Locator = (By.XPATH, "//h1[normalize-space()='Error!']", 5)
    ERROR_MESSAGE: Locator = (By.XPATH, "//p[@class='error']", 5)

    error_message_empty_fields = "Please enter a username and password."
    error_message_invalid_credentials = (
        "The username and password could not be verified."
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def login(self, username: str, password: str) -> None:
        self.click(self.USERNAME_FIELD)
        self.input_text(self.USERNAME_FIELD, username)
        self.click(self.PASSWORD_FIELD)
        self.input_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def get_greeting_message(self) -> str:
        result: str = self.get_text(self.GREETING_MESSAGE)
        return result

    def is_error_title_located(self) -> bool:
        result: bool = self.is_element_located(self.ERROR_TITLE)
        return result
