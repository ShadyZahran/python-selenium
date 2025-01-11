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
