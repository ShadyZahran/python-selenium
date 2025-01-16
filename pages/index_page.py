import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.login_page import ParabankLoginSection

logger = logging.getLogger(__name__)


class ParabankIndexPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://parabank.parasoft.com/parabank/index.htm"
        self.login_section = ParabankLoginSection(self.driver)
