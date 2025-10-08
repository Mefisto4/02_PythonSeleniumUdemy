"""
Contains _BaseControl class as a creator class for Base Controls factory pattern
"""

from abc import ABC
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class _BaseControl(ABC):
    """
    _BaseControl class as a parent (factory) for all controls in the framework.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        self.driver = driver
        self.locator = locator
        self.web_element: WebElement = self.driver.find_element(*self.locator)
        self.wait = WebDriverWait(self.driver, 5)

    def __str__(self) -> str:
        return f"<WebElement: {self.locator}>"

    @staticmethod
    def pre_action(func):
        """
        Decorator function for pre-action.
        """

        def wrapper(self, *args, **kwargs):
            """
            Wait for the element to be present in order to perform actions.
            """
            if self.wait.until(expected_conditions.presence_of_element_located(self.locator)):
                return func(self, *args, **kwargs)
            raise AttributeError(f"{self} is not present")

        return wrapper

    def is_displayed(self) -> bool:
        """
        Checks if element is displayed.

        :return: True if element is displayed, False otherwise.
        """
        return self.web_element.is_displayed()

    @pre_action
    def click(self) -> None:
        """
        Clicks element.

        :return:
        """
        self.web_element.click()
