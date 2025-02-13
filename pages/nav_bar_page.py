import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator

logger = logging.getLogger(__name__)


class NavBar(BasePage):
    HOME_BUTTON: Locator = (By.CSS_SELECTOR, ".nav-link[data-test='nav-home']", 5)
    CONTACT_BUTTON: Locator = (By.CSS_SELECTOR, ".nav-link[data-test='nav-contact']", 5)
    SIGNIN_BUTTON: Locator = (By.CSS_SELECTOR, ".nav-link[data-test='nav-sign-in']", 5)
    USER_MENU: Locator = (By.CSS_SELECTOR, "a[data-test='nav-menu']", 5)

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def click_home_button(self) -> None:
        self.click(self.HOME_BUTTON)

    def click_contact_button(self) -> None:
        self.click(self.CONTACT_BUTTON)

    def click_signin_button(self) -> None:
        self.click(self.SIGNIN_BUTTON)

    def click_user_menu(self) -> None:
        self.click(self.USER_MENU)

    def get_signed_in_username(self) -> str:
        return self.get_text(self.USER_MENU)
