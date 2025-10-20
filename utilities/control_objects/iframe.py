"""
Represents frame controls (HTML page embedded into another HTML page, i.e.: <iframe>).
"""

from typing import Tuple, Type

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


class IFrame:
    """
    Represents iframe elements - here: handled by context manager.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str], page: Type[BasePage]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "iframe[title='HTML iFrame']")
        :param page: embedded page
        """
        self.driver = driver
        self.locator = locator
        self.web_element: WebElement = self.driver.find_element(*self.locator)
        self.page = page

    def __enter__(self) -> BasePage:
        self.driver.switch_to.frame(self.web_element)
        return self.page(driver=self.driver, url=self.page.URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.switch_to.default_content()
