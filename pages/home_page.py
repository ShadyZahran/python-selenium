import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.nav_bar_page import NavBar

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://practicesoftwaretesting.com/"
        self.nav_bar = NavBar(self.driver)
