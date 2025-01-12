import logging

from base_page import BasePage, Locator
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class ParabankLoginSection(BasePage):
    USERNAME_FIELD: Locator = (By.XPATH, "//input[@name='username']", 5)
    PASSWORD_FIELD: Locator = (By.XPATH, "//input[@name='password']", 5)
    LOGIN_BUTTON: Locator = (By.XPATH, "//input[@value='Log In']", 5)

    GREETING_MESSAGE: Locator = (By.XPATH, "//p[@class='smallText']", 5)
    ERROR_TITLE: Locator = (By.XPATH, "//h1[normalize-space()='Error!']", 5)
    ERROR_MESSAGE: Locator = (By.XPATH, "//p[@class='error']", 5)

    login_error_message_empty_fields = "Please enter a username and password."
    login_error_message_invalid_credentials = (
        "The username and password could not be verified."
    )

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.click(self.USERNAME_FIELD)
        self.input_text(self.USERNAME_FIELD, username)
        self.click(self.PASSWORD_FIELD)
        self.input_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def get_greeting_message(self) -> str:
        return self.get_text(self.GREETING_MESSAGE)

    def is_error_title_located(self) -> bool:
        return self.is_element_located(self.ERROR_TITLE)

    def is_error_message_invalid_credentials(self) -> bool:
        return (
            self.get_text(self.ERROR_MESSAGE)
            == self.login_error_message_invalid_credentials
        )

    def is_error_message_empty_fields(self) -> bool:
        return (
            self.get_text(self.ERROR_MESSAGE) == self.login_error_message_empty_fields
        )
