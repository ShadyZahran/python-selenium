import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator
from pages.nav_bar_page import NavBar

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    EMAIL_INPUT: Locator = (By.ID, "email", 5)
    PASSWORD_INPUT: Locator = (By.ID, "password", 5)
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "[data-test='login-submit']", 5)

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://practicesoftwaretesting.com/auth/login"
        self.nav_bar = NavBar(self.driver)

    def fill_email(self, email: str) -> None:
        self.click(self.EMAIL_INPUT)
        self.input_text(self.EMAIL_INPUT, email)

    def fill_password(self, password: str) -> None:
        self.click(self.PASSWORD_INPUT)
        self.input_text(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.fill_email(username)
        self.fill_password(password)
        self.click_login()
