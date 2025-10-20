"""
Represents simple elements that allow to input and display text.
"""

from utilities.control_objects.base_control import _BaseControl


class Textbox(_BaseControl):
    """
    Represents textbox elements.
    """

    def get_text(self) -> str:
        """
        Gets text from textbox.

        :return: displayed text
        """
        value = self.web_element.get_attribute("value")
        if isinstance(value, str):
            return value
        raise AttributeError(f"Could not retrieve 'value' attribute for {self}")

    @_BaseControl.pre_action
    def set_text(self, value) -> None:
        """
        Sets text in textbox.

        :param value: text to be set
        :return: None
        """
        self.web_element.clear()
        self.web_element.send_keys(value)
        if (text := self.get_text()) != value:
            raise ValueError(f"Text was not set. Actual: {text}; Expected: {value}")
