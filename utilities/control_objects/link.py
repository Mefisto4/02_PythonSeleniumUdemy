"""
Represents hyperlink controls.
"""

from utilities.control_objects.base_control import _BaseControl


class Link(_BaseControl):
    """
    Represents hyperlink <a> elements.
    """

    def get_text(self) -> str:
        """
        Gets text from hyperlink.

        :return: string text from label
        """
        return self.web_element.text

    def get_href(self) -> str:
        """
        Gets Hypertext Reference (HREF) attribute from hyperlink.

        :return: URL of the page the hyperlink goes to
        """
        value = self.web_element.get_attribute("href")
        if isinstance(value, str):
            return value
        raise AttributeError(f"Could not retrieve 'href' attribute for {self}")
