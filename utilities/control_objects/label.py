"""
Represents read-only controls.
"""

from utilities.control_objects.base_control import _BaseControl


class Label(_BaseControl):
    """
    Represents label elements.
    """

    def get_text(self) -> str:
        """
        Gets text from label.

        :return: string text from label
        """
        return self.web_element.text
