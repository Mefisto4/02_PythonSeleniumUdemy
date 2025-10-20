"""
Represents table controls.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple, Type

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utilities.control_objects.base_control import _BaseControl


class Table(_BaseControl):
    """
    Represents HTML table.
    """

    def __init__(self, driver: WebDriver, locator: Tuple[str, str], strategy: Type[_TableStrategy]) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param locator: pair of By strategy and locator, i.e.: (By.CSS_SELECTOR, "input[value='admin']")
        """
        super().__init__(driver, locator)
        self._strategy = strategy()

    def get_headers(self) -> List[str] | None:
        """
        Gets headers of table if present.

        :return: list of header values
        """
        return self._strategy.get_headers(self.web_element)

    def get_body(self) -> List[List[str]] | None:
        """
        Gets body of table.

        :return: list of rows, where each row represents a table data
        """
        return self._strategy.get_body(self.web_element)

    def get_table(self) -> List[List[str]]:
        """
        Gets all values from table.

        :return: list of rows, where each row is a list of cell values (with headers included)
        """
        result = []
        if headers := self.get_headers():
            result.append(headers)
        if body := self.get_body():
            result.extend(body)
        return result


class _TableStrategy(ABC):
    """
    Abstract class as a table strategy interface.
    """

    @abstractmethod
    def get_headers(self, web_element: WebElement) -> List[str] | None:
        """
        Gets headers of table if present.

        :param web_element: web element of <table>
        :return: list of header values
        """

    @abstractmethod
    def get_body(self, web_element: WebElement) -> List[List[str]] | None:
        """
        Gets body of table if present.

        :param web_element: web element of <table>
        :return: list of rows, where each row represents a table data
        """


class SimpleTableStrategy(_TableStrategy):
    """
    Represents simple HTML table (table rows + table data).

    Example:
        <table>
            ...
            <tr>
                <td>Chris</td>
                <td>HTML tables</td>
                <td>22</td>
            </tr>
            <tr>
                ...
            </tr>
            ...
        </table>
    """

    def get_headers(self, web_element: WebElement) -> List[str] | None:
        return None

    def get_body(self, web_element: WebElement) -> List[List[str]] | None:
        body = []
        for row in web_element.find_elements(By.CSS_SELECTOR, "tr"):
            body.append([cell.text for cell in row.find_elements(By.CSS_SELECTOR, "td")])
        return body


class HeadingsTableStrategy(_TableStrategy):
    """
    Represents HTML table with table headings in the first row.

    Example:
        <table>
            ...
            <tr>
                <th>Person</th>
                <th>Most interested in</th>
                <th>Age</th>
            </tr>
            <tr>
                <td>Chris</td>
                <td>HTML tables</td>
                <td>22</td>
            </tr>
            <tr>
                ...
            </tr>
            ...
        </table>
    """

    def get_headers(self, web_element: WebElement) -> List[str] | None:
        header = web_element.find_element(By.CSS_SELECTOR, "tr:first-child")
        return [header.text for header in header.find_elements(By.CSS_SELECTOR, "th")]

    def get_body(self, web_element: WebElement) -> List[List[str]] | None:
        body = []
        for row in web_element.find_elements(By.CSS_SELECTOR, "tr:nth-child(n+2)"):
            body.append([cell.text for cell in row.find_elements(By.CSS_SELECTOR, "td")])
        return body


class HeaderBodyTableStrategy(_TableStrategy):
    """
    Represents HTML table with separate table header and table main body.

    Example:
        <table>
            ...
            <thead>
                <tr>
                    <th scope="col">Person</th>
                    <th scope="col">Most interested in</th>
                    <th scope="col">Age</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Chris</td>
                    <td>HTML tables</td>
                    <td>22</td>
                </tr>
                <tr>...</tr>
            </tbody>
            ...
        </table>
    """

    def get_headers(self, web_element: WebElement) -> List[str] | None:
        """
        Gets table headers <th> inside <thead> tag.

        :return: list of table headers if <thead> tag exists, None otherwise.
        """
        header = web_element.find_element(By.CSS_SELECTOR, "thead")
        if not header:
            return None
        return [header.text for header in header.find_elements(By.CSS_SELECTOR, "th")]

    def get_body(self, web_element: WebElement) -> List[List[str]] | None:
        table_body = web_element.find_element(By.CSS_SELECTOR, "tbody")
        if not table_body:
            return None
        body = []
        for row in table_body.find_elements(By.CSS_SELECTOR, "tr"):
            body.append([cell.text for cell in row.find_elements(By.CSS_SELECTOR, "td")])
        return body


class MixedTableStrategy(_TableStrategy):
    """
    Represents HTML table where table headings can be mixed with table data in the table row.

    Example:
        <table>
            ...
            <tr>
                <th>Person</th>
                <td>Most interested in</td>
                <td>Age</td>
            </tr>
            <tr>
                <th>Chris</th>
                <td>HTML tables</td>
                <td>22</td>
            </tr>
            <tr>
                ...
            </tr>
            ...
        </table>
    """

    def get_headers(self, web_element: WebElement) -> List[str] | None:
        raise NotImplementedError()

    def get_body(self, web_element: WebElement) -> List[List[str]] | None:
        raise NotImplementedError()
