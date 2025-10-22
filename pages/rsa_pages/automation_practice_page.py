"""
Contains AutomationPractice page objects.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.rsa_pages import AUTOMATION_PRACTICE
from pages.rsa_pages.rahulshettyacademy_page import RahulShettyAcademyPage
from utilities.control_objects.button import Button
from utilities.control_objects.checkbox_radiobutton import Checkbox, Radiobutton
from utilities.control_objects.dropdown import DropdownDynamic, DropdownStatic
from utilities.control_objects.iframe import IFrame
from utilities.control_objects.label import Label
from utilities.control_objects.link import Link
from utilities.control_objects.table import HeaderBodyTableStrategy, HeadingsTableStrategy, Table
from utilities.control_objects.textbox import Textbox


class AutomationPracticePage(BasePage):
    """
    Web page for automation practice of basic controls.
    """

    # pylint: disable=too-many-public-methods

    URL = AUTOMATION_PRACTICE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)
        self._locators = _AutomationPracticePageLocators

    @property
    def radiobutton_1(self) -> Radiobutton:
        """
        Returns 'Radio1' radiobutton.

        :return: Radiobutton
        """
        return Radiobutton(self.driver, self._locators.RADIOBUTTON_1)

    @property
    def radiobutton_2(self) -> Radiobutton:
        """
        Returns 'Radio2' radiobutton.

        :return: Radiobutton
        """
        return Radiobutton(self.driver, self._locators.RADIOBUTTON_2)

    @property
    def radiobutton_3(self) -> Radiobutton:
        """
        Returns 'Radio3' radiobutton.

        :return: Radiobutton
        """
        return Radiobutton(self.driver, self._locators.RADIOBUTTON_3)

    @property
    def dropdown_dynamic(self) -> DropdownDynamic:
        """
        Returns dynamic (auto-suggested) dropdown.

        :return: DropdownDynamic
        """
        return DropdownDynamic(
            driver=self.driver,
            dropdown_locator=self._locators.DYNAMIC_DROPDOWN,
            dropdown_list_locator=self._locators.DYNAMIC_DROPDOWN_LIST,
            dropdown_list_item_locator=self._locators.DYNAMIC_DROPDOWN_LIST_ITEM,
        )

    @property
    def dropdown_static(self) -> DropdownStatic:
        """
        Returns static dropdown.

        :return: DropdownStatic
        """
        return DropdownStatic(self.driver, self._locators.STATIC_DROPDOWN)

    @property
    def checkbox_1(self) -> Checkbox:
        """
        Returns 'Option1' checkbox.

        :return: Checkbox
        """
        return Checkbox(self.driver, self._locators.CHECKBOX_1)

    @property
    def checkbox_2(self) -> Checkbox:
        """
        Returns 'Option2' checkbox.

        :return: Checkbox
        """
        return Checkbox(self.driver, self._locators.CHECKBOX_2)

    @property
    def checkbox_3(self) -> Checkbox:
        """
        Returns 'Option3' checkbox.

        :return: Checkbox
        """
        return Checkbox(self.driver, self._locators.CHECKBOX_3)

    @property
    def open_window_button(self) -> Button:
        """
        Returns 'Open Window' button.

        :return: Button
        """
        return Button(self.driver, self._locators.OPEN_WINDOW_BUTTON)

    @property
    def open_tab_button(self) -> Button:
        """
        Returns 'Open Tab' button.

        :return: Button
        """
        return Button(self.driver, self._locators.OPEN_TAB_BUTTON)

    @property
    def alert_textbox(self) -> Textbox:
        """
        Returns alert example textbox.

        :return: Textbox
        """
        return Textbox(self.driver, self._locators.ALERT_TEXTBOX)

    @property
    def alert_button(self) -> Button:
        """
        Returns 'Alert' button.

        :return: Button
        """
        return Button(self.driver, self._locators.ALERT_BUTTON)

    @property
    def popup_button(self) -> Button:
        """
        Returns 'Confirm' button.

        :return: Button
        """
        return Button(self.driver, self._locators.POPUP_BUTTON)

    @property
    def table_static(self) -> Table:
        """
        Returns 'Web Table Example' table.

        :return: Table
        """
        return Table(self.driver, self._locators.WEB_TABLE_STATIC, HeadingsTableStrategy)

    @property
    def table_fixed_header(self) -> Table:
        """
        Returns 'Web Table Fixed header' table.

        :return: Table
        """
        return Table(self.driver, self._locators.WEB_TABLE_FIXED_HEADER, HeaderBodyTableStrategy)

    @property
    def table_fixed_label(self) -> Label:
        """
        Returns 'Web Table Fixed header' footer label.

        :return: Label
        """
        return Label(self.driver, self._locators.WEB_TABLE_FIXED_HEADER_LABEL)

    @property
    def hide_button(self) -> Button:
        """
        Returns 'Hide' button.

        :return: Button
        """
        return Button(self.driver, self._locators.HIDE_BUTTON)

    @property
    def show_button(self) -> Button:
        """
        Returns 'Show' button.

        :return: Button
        """
        return Button(self.driver, self._locators.SHOW_BUTTON)

    @property
    def hide_show_textbox(self) -> Textbox:
        """
        Returns 'Hide/Show Example' textbox.

        :return: Textbox
        """
        return Textbox(self.driver, self._locators.HIDE_SHOW_TEXTBOX)

    @property
    def mouse_hover_button(self) -> Button:
        """
        Returns 'Mouse Hover' button.

        :return: Button
        """
        return Button(self.driver, self._locators.MOUSE_HOVER_BUTTON)

    @property
    def mouse_hover_content_top(self) -> Label:
        """
        Returns 'Mouse Hover' list content label.

        :return: Label
        """
        return Label(self.driver, self._locators.MOUSE_HOVER_CONTENT_TOP)

    @property
    def mouse_hover_content_reload(self) -> Label:
        """
        Returns 'Mouse Hover' list content label.

        :return: Label
        """
        return Label(self.driver, self._locators.MOUSE_HOVER_CONTENT_RELOAD)

    @property
    def iframe(self) -> IFrame:
        """
        Returns 'iFrame Example' iframe.

        :return: IFrame
        """
        return IFrame(self.driver, self._locators.IFRAME, RahulShettyAcademyPage)

    @property
    def blinking_text_link(self) -> Link:
        """
        Returns blinking text link.

        :return: Link
        """
        return Link(self.driver, self._locators.BLINKING_TEXT_LINK)


class _AutomationPracticePageLocators:
    """
    Contains locators for AutomationPracticePage.
    """

    # pylint: disable=too-few-public-methods

    RADIOBUTTON_1 = (By.CSS_SELECTOR, "input[value='radio1']")
    RADIOBUTTON_2 = (By.CSS_SELECTOR, "input[value='radio2']")
    RADIOBUTTON_3 = (By.CSS_SELECTOR, "input[value='radio3']")

    DYNAMIC_DROPDOWN = (By.ID, "autocomplete")
    DYNAMIC_DROPDOWN_LIST = (By.CSS_SELECTOR, "#ui-id-1 li")
    DYNAMIC_DROPDOWN_LIST_ITEM = (By.XPATH, "//li[@class='ui-menu-item']/div[text()='{}']")

    STATIC_DROPDOWN = (By.ID, "dropdown-class-example")

    CHECKBOX_1 = (By.ID, "checkBoxOption1")
    CHECKBOX_2 = (By.ID, "checkBoxOption2")
    CHECKBOX_3 = (By.ID, "checkBoxOption3")

    OPEN_WINDOW_BUTTON = (By.ID, "openwindow")
    OPEN_TAB_BUTTON = (By.ID, "opentab")

    ALERT_TEXTBOX = (By.ID, "name")
    ALERT_BUTTON = (By.ID, "alertbtn")
    POPUP_BUTTON = (By.ID, "confirmbtn")

    WEB_TABLE_STATIC = (By.CSS_SELECTOR, ".table-display")
    WEB_TABLE_FIXED_HEADER = (By.CSS_SELECTOR, ".tableFixHead table")
    WEB_TABLE_FIXED_HEADER_LABEL = (By.XPATH, "/html/body/div[3]/div[2]/fieldset[2]/div[2]")

    HIDE_BUTTON = (By.ID, "hide-textbox")
    SHOW_BUTTON = (By.ID, "show-textbox")
    HIDE_SHOW_TEXTBOX = (By.ID, "displayed-text")

    MOUSE_HOVER_BUTTON = (By.ID, "mousehover")
    MOUSE_HOVER_CONTENT_TOP = (By.XPATH, "//a[text()='Top']")
    MOUSE_HOVER_CONTENT_RELOAD = (By.XPATH, "//a[text()='Reload']")

    IFRAME = (By.ID, "courses-iframe")

    BLINKING_TEXT_LINK = (By.CSS_SELECTOR, ".blinkingText")
