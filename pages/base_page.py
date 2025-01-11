import logging
from typing import TypeAlias

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

Locator: TypeAlias = tuple[
    str, str, int
]  # strategy, value, timeout -> example: (By.XPATH, "//input[@name='username']", 5)


class BasePage:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def load(self, url):
        logger.info(f"Loading {url}")
        self.driver.get(url)

    def find_element(self, locator: Locator) -> WebElement:
        if self.is_element_located(locator):
            logger.info(f"Element located: {locator[0]}={locator[1]}")
            return self.driver.find_element(*locator[:2])
        else:
            raise Exception(f"Element not found: {locator[0]}={locator[1]}")

    def click(self, locator: Locator):
        element = self.find_element(locator)
        if self.is_element_clickable(locator):
            logger.info(f"Clicking element: {locator[0]}={locator[1]}")
            element.click()
        else:
            raise Exception(f"Element not clickable: {locator[0]}={locator[1]}")

    def input_text(self, locator: Locator, text: str):
        element = self.find_element(locator)
        logger.info(f"Typing '{text}' into element: {locator[0]}={locator[1]}")
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        element = self.find_element(locator)
        logger.info(f"Getting text from element: {locator[0]}={locator[1]}")
        return element.text

    def is_element_located(self, locator: Locator) -> bool:
        try:
            WebDriverWait(self.driver, locator[2]).until(
                EC.presence_of_element_located(locator[:2])
            )
        except Exception:
            return False
        else:
            return True

    def is_element_clickable(self, locator: Locator) -> bool:
        try:
            WebDriverWait(self.driver, locator[2], 1).until(
                EC.element_to_be_clickable(locator[:2])
            )
        except Exception:
            return False
        else:
            return True
