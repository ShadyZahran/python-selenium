import logging

from base_page import BasePage
from login_page import ParabankLoginSection

logger = logging.getLogger(__name__)


class ParabankIndexPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://parabank.parasoft.com/parabank/index.htm"
        self.login_section = ParabankLoginSection(self.driver)

    def load(self) -> "ParabankIndexPage":
        super().load(self.url)
        return self
