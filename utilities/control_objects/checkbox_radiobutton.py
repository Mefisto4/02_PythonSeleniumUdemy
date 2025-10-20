"""
Represents checkable elements.
"""

from selenium.webdriver.support import expected_conditions

from utilities.control_objects.base_control import _BaseControl


class _SelectOptionControl(_BaseControl):
    """
    Represents checkable elements for option selection.
    """

    @staticmethod
    def pre_action(func):
        """
        Decorator function for pre action.
        """

        def wrapper(self, *args, **kwargs):
            """
            Wait for the element to be present in order to perform actions.
            """
            if self.wait.until(expected_conditions.element_to_be_clickable(self.locator)):
                return func(self, *args, **kwargs)
            raise AttributeError(f"{self} is not present")

        return wrapper

    def is_checked(self) -> bool:
        """
        Checks if element is checked.

        :return: True if element is checked, False otherwise.
        """
        return self.web_element.is_selected()

    @pre_action
    def select(self) -> None:
        """
        Selects element if not selected. Does nothing otherwise.

        :return: None
        """
        if not self.is_checked():
            self.web_element.click()


class Radiobutton(_SelectOptionControl):
    """
    Represents radiobutton - element that allows to select only one option from a set.
    """


class Checkbox(_SelectOptionControl):
    """
    Represents checkbox - element that allows to select multiple options from a set.
    """

    @_SelectOptionControl.pre_action
    def deselect(self) -> None:
        """
        Deselects checkbox if selected. Does nothing otherwise.

        :return: None
        """
        if self.is_checked():
            self.web_element.click()
