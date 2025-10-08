"""
Represents interactable elements that allow to make a selection using expandable list of values.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utilities.base_controls.base_control import _BaseControl


class _Dropdown(_BaseControl):
    """
    Represents dropdown elements.
    """


class DropdownStatic(_Dropdown):
    """
    Represents static dropdown elements - list of values is fixed and predetermined.
    """

    @_BaseControl.pre_action
    def select(self, value: str) -> None:
        """
        Selects dropdown value based on visible text.

        :param value:
        :return: None
        """
        dropdown = Select(self.web_element)
        dropdown.select_by_visible_text(value)


class DropdownDynamic(_Dropdown):
    """
    Represents dynamic dropdown elements - list of values can change, expand or be auto-suggestive.
    """

    def __init__(
        self,
        driver: WebDriver,
        dropdown_locator: Tuple[str, str],
        dropdown_list_locator: Tuple[str, str],
        dropdown_list_item_locator: Tuple[str, str],
    ) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param dropdown_locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        :param dropdown_list_locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        :param dropdown_list_item_locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, dropdown_locator)
        self.dropdown_list_locator = dropdown_list_locator
        self.dropdown_list_item_locator = dropdown_list_item_locator

    def _start_typing(self, value: str) -> None:
        self.web_element.clear()
        self.web_element.send_keys(value)

    def _wait_for_suggestions(self) -> None:
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.wait.until(
            expected_conditions.all_of(lambda x: len(self.driver.find_elements(*self.dropdown_list_locator)) > 0)
        )

    def _select_option(self, value: str) -> None:
        self.driver.find_element(
            self.dropdown_list_item_locator[0],
            self.dropdown_list_item_locator[1].format(value),
        ).click()

    @_BaseControl.pre_action
    def select(self, value: str) -> None:
        """
        Select an option from the dropdown.

        :param value: option to select
        :return: None
        """
        self._start_typing(value)
        self._wait_for_suggestions()
        self._select_option(value)

    @_BaseControl.pre_action
    def select_by_partial_value(self, value: str, char_num: int) -> None:
        """
        Select an option from the dropdown by typing only part of the option text.

        :param value: option to select
        :param char_num: how many first characters to type
        :return: None
        """
        self._start_typing(value.lower()[:char_num])
        self._wait_for_suggestions()
        self._select_option(value)
