"""
Contains RahulShettyAcademy main page objects.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.rsa_pages import MAIN_PAGE
from utilities.control_objects.link import Link


class RahulShettyAcademyPage(BasePage):
    """
    Main page of Rahul Shetty Academy.
    """

    URL = MAIN_PAGE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)
        self._locators = _RahulShettyAcademyPageLocators

    @property
    def courses_link(self) -> Link:
        """
        Returns link to courses page.

        :return: Link
        """
        return Link(self.driver, self._locators.COURSES_LINK)


class _RahulShettyAcademyPageLocators:
    """
    Contains locators for RahulShettyAcademyPage.
    """

    # pylint: disable=too-few-public-methods
    COURSES_LINK = (By.XPATH, "//a[text()='Courses']")
