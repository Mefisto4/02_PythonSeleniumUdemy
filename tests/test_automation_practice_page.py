"""
Framework test of base controls.
"""

import pytest
from selenium.common import NoSuchElementException

from pages.rsa_pages.automation_practice_page import AutomationPracticePage
from pages.rsa_pages.rahulshettyacademy_page import RahulShettyAcademyPage


@pytest.fixture
def class_fixture(request, test_fixture):
    """
    Setup test specific fixture.
    """
    request.cls.tools = test_fixture
    request.cls.driver = request.cls.tools.driver
    request.cls.page = AutomationPracticePage(request.cls.driver)


@pytest.mark.framework
@pytest.mark.usefixtures("class_fixture")
class TestAutomationPracticePage:
    """
    Test Automation Practice page.
    """

    # pylint: disable=no-member,too-many-public-methods
    def test_go_to_practice_page(self):
        """Test if page opens."""
        self.page.go_to()
        assert self.page.get_title() == "Practice Page"

    @pytest.mark.parametrize(
        "radiobutton, expected_states",
        [
            ("default", (False, False, False)),
            ("radiobutton_1", (True, False, False)),
            ("radiobutton_2", (False, True, False)),
            ("radiobutton_3", (False, False, True)),
        ],
    )
    def test_radiobuttons(self, radiobutton, expected_states):
        """Test radiobutton group set."""
        if radiobutton != "default":
            getattr(self.page, radiobutton).click()
        assert (
            self.page.radiobutton_1.is_checked(),
            self.page.radiobutton_2.is_checked(),
            self.page.radiobutton_3.is_checked(),
        ) == expected_states

    def test_dropdown_dynamic_default(self):
        """Test initial state of dynamic dropdown."""
        assert self.page.dropdown_dynamic.get_text() == "Type to Select Countries"

    def test_dropdown_dynamic_select(self):
        """Test select by full value in dynamic dropdown."""
        self.page.dropdown_dynamic.select("Poland")
        assert self.page.dropdown_dynamic.get_text() == "Poland"

    @pytest.mark.xfail(raises=AssertionError, reason="Unexpected behavior on this site.")
    def test_dropdown_dynamic_select_by_partial_value(self):
        """Test select by partial value in dynamic dropdown."""
        self.page.dropdown_dynamic.select_by_partial_value("India", 3)
        assert self.page.dropdown_dynamic.get_text() == "India"

    def test_dynamic_dropdown_incorrect_select_value(self):
        """Test dynamic dropdown incorrect select value."""
        with pytest.raises(NoSuchElementException):
            self.page.dropdown_dynamic.select("123")

    def test_dropdown_static_default(self):
        """Test initial state of static dropdown."""
        assert self.page.dropdown_static.get_text() == "Select"

    def test_dropdown_static_select(self):
        """Test select value in static dropdown."""
        self.page.dropdown_static.select("Option2")
        assert self.page.dropdown_static.get_text() == "Option2"

    @pytest.mark.parametrize(
        "checkbox, expected_states",
        [
            ("default", (False, False, False)),
            ("checkbox_1", (True, False, False)),
            ("checkbox_2", (True, True, False)),
            ("checkbox_3", (True, True, True)),
            ("checkbox_2", (True, False, True)),
        ],
    )
    def test_checkboxes(self, checkbox, expected_states):
        """Test checkbox group set."""
        if checkbox != "default":
            getattr(self.page, checkbox).click()
        assert (
            self.page.checkbox_1.is_checked(),
            self.page.checkbox_2.is_checked(),
            self.page.checkbox_3.is_checked(),
        ) == expected_states

    def test_switch_window(self):
        """Test switching between browser windows."""
        assert len(self.driver.window_handles) == 1, "Only 1 window should be opened."
        self.page.open_window_button.click()
        try:
            self.tools.wait.until(lambda x: len(self.driver.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.tools.wait.until(
                self.tools.ec.title_is("QAClick Academy - A Testing Academy to Learn, Earn and Shine")
            )
            assert self.driver.current_url == "https://www.qaclickacademy.com/"
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def test_switch_tab(self):
        """Test switching between browser tabs."""
        assert len(self.driver.window_handles) == 1, "Only 1 tab should be opened."
        self.page.open_window_button.click()
        try:
            self.tools.wait.until(lambda x: len(self.driver.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.tools.wait.until(
                self.tools.ec.title_is("QAClick Academy - A Testing Academy to Learn, Earn and Shine")
            )
            assert self.driver.current_url == "https://www.qaclickacademy.com/"
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def test_alert(self):
        """Test webpage's JavaScript alert window."""
        msg = "TEXT 1"
        self.page.alert_textbox.set_text(msg)
        self.page.alert_button.click()
        try:
            assert self.driver.switch_to.alert.text == f"Hello {msg}, share this practice page and share your knowledge"
        finally:
            self.driver.switch_to.alert.dismiss()

    def test_popup(self):
        """Test webpage's JavaScript confirm window."""
        msg = "TEXT 2"
        self.page.alert_textbox.set_text(msg)
        self.page.popup_button.click()
        try:
            assert self.driver.switch_to.alert.text == f"Hello {msg}, Are you sure you want to confirm?"
        finally:
            self.driver.switch_to.alert.accept()

    def test_web_table_get_headers(self):
        """Test reading headers from web table with headings."""
        headers = self.page.table_static.get_headers()
        assert headers == ["Instructor", "Course", "Price"]

    def test_web_table_get_body(self):
        """Test reading body from web table with headings."""
        body = self.page.table_static.get_body()
        assert body[2][1] == "Appium (Selenium) - Mobile Automation Testing from Scratch"

    def test_web_table_get_table(self):
        """Test reading whole content from web table with headings."""
        table = self.page.table_static.get_table()
        assert table[0][2] == "Price"
        assert table[3][1] == "Appium (Selenium) - Mobile Automation Testing from Scratch"

    def test_web_table_fixed_get_headers(self):
        """Test reading headers from web table with <thead> and <tbody>."""
        headers = self.page.table_fixed_header.get_headers()
        assert headers == ["Name", "Position", "City", "Amount"]

    def test_web_table_fixed_get_body(self):
        """Test reading body from web table with <thead> and <tbody>."""
        body = self.page.table_fixed_header.get_body()
        assert body[4][1] == "Engineer"

    def test_web_table_fixed_get_table(self):
        """Test reading whole content from web table with <thead> and <tbody>."""
        table = self.page.table_fixed_header.get_table()
        assert table[0][2] == "City"
        assert table[5][1] == "Engineer"

    def test_web_table_label(self):
        """Test label."""
        assert self.page.table_fixed_label.get_text() == "Total Amount Collected: 296"

    def test_element_displayed_default_state(self):
        """Test default state of hide/show textbox."""
        assert self.page.hide_show_textbox.is_displayed()

    def test_element_displayed_hide(self):
        """Test textbox hide option."""
        self.page.hide_button.click()
        assert not self.page.hide_show_textbox.is_displayed()

    def test_element_displayed_show(self):
        """Test textbox show option."""
        self.page.show_button.click()
        assert self.page.hide_show_textbox.is_displayed()

    def test_mouse_hover_default_state(self):
        """Test default state of display-element-on-hover object."""
        self.page.scroll(int(self.page.mouse_hover_button.web_element.location["x"] * 1.1))
        assert self.page.mouse_hover_button.is_displayed()
        assert not self.page.mouse_hover_content_top.is_displayed()
        assert not self.page.mouse_hover_content_reload.is_displayed()

    def test_mouse_hover_mouse_move_action(self):
        """Test 'on hover' action of display-element-on-hover object."""
        self.page.mouse_hover_button.hover_over()
        assert self.page.mouse_hover_content_top.is_displayed()
        assert self.page.mouse_hover_content_reload.is_displayed()

    def test_mouse_hover_top_option(self):
        """Test 'top' option of display-element-on-hover object."""
        curr_pos = self.driver.execute_script("return window.pageYOffset;")
        self.page.mouse_hover_content_top.click()
        assert self.driver.execute_script("return window.pageYOffset;") != curr_pos

    def test_mouse_hover_reload_option(self):
        """Test 'reload' option of display-element-on-hover object."""
        self.page.checkbox_3.select()
        self.page.scroll(int(self.page.mouse_hover_button.web_element.location["x"] * 1.1))
        self.page.mouse_hover_button.hover_over()
        self.page.mouse_hover_content_reload.click()
        assert not self.page.checkbox_3.is_checked()

    def test_iframe_outer_scope_before(self):
        """Test that iframe's webpage is not accessible outside iframe."""
        iframe_page = RahulShettyAcademyPage(self.driver)
        with pytest.raises(NoSuchElementException):
            assert not iframe_page.courses_link.is_present()

    def test_iframe_context_manager(self):
        """Test that iframe's webpage is accessible inside iframe."""
        with self.page.iframe as frame:
            assert frame.courses_link.is_present()
            assert frame.courses_link.get_href() == "https://courses.rahulshettyacademy.com/courses"

    def test_iframe_outer_scope_after(self):
        """Test that iframe's webpage is still not accessible outside iframe."""
        iframe_page = RahulShettyAcademyPage(self.driver)
        with pytest.raises(NoSuchElementException):
            assert not iframe_page.courses_link.is_present()
