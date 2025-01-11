import logging

from login_page import ParabankLoginSection, Locator
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class ParabankIndexPage(ParabankLoginSection):
    USERNAME_FIELD: Locator = (By.XPATH, "//input[@name='username']", 5)

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://parabank.parasoft.com/parabank/index.htm"

    def load(self) -> "ParabankIndexPage":
        super().load(self.url)
        return self
