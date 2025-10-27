"""
Unit tests for control objects (./utilities/control_objects/*)
"""

import pytest
from selenium.webdriver.common.by import By

from pages.rsa_pages.automation_practice_page import AutomationPracticePage
from utilities.control_objects.table import MixedTableStrategy, SimpleTableStrategy, Table


@pytest.fixture
def class_fixture(request, test_fixture):
    """
    Setup test specific fixture.
    """
    request.cls.tools = test_fixture
    request.cls.driver = request.cls.tools.driver
    request.cls.page = AutomationPracticePage(request.cls.driver)
    request.cls.page.go_to()


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestBaseControl:
    """
    Test BaseControl object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.hide_button  # pylint: disable=no-member

    def test_printing(self, control):
        """Test __str__ method."""
        assert str(control) == f"<WebElement: {control.locator}>"

    def test_is_displayed(self, control):
        """Test is_displayed() method."""
        assert control.is_displayed()

    def test_is_enabled(self, control):
        """Test is_enabled() method."""
        assert control.is_enabled()

    def test_is_present(self, control):
        """Test is_present() method."""
        assert control.is_present()

    def test_click(self, control):
        """Test click() method."""
        control.click()
        assert not self.page.hide_show_textbox.is_displayed()  # pylint: disable=no-member

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_hover_over(self, control):
        """Test hover_over() method."""
        raise NotImplementedError


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestButton:
    """
    Test Button object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.hide_button  # pylint: disable=no-member

    @pytest.mark.skip(reason="no methods to test")
    def test_dummy(self, control):
        """PLACEHOLDER"""
        assert control


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestSelectOptionControl:
    """
    Test SelectOptionControl object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.radiobutton_1  # pylint: disable=no-member

    def test_is_checked(self, control):
        """Test is_checked() method."""
        assert not control.is_checked()

    def test_select(self, control):
        """Test select() method."""
        control.select()
        assert control.is_checked()


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestRadiobutton:
    """
    Test Radiobutton object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.radiobutton_1  # pylint: disable=no-member

    @pytest.mark.skip(reason="no methods to test")
    def test_dummy(self, control):
        """PLACEHOLDER"""
        assert control


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestCheckbox:
    """
    Test Checkbox object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.checkbox_1  # pylint: disable=no-member

    def test_deselect(self, control):
        """Test deselect() method."""
        control.select()
        control.deselect()
        assert not control.is_checked()


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestStaticDropdown:
    """
    Test StaticDropdown object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.dropdown_static  # pylint: disable=no-member

    def test_get_text(self, control):
        """Test get_text() method."""
        assert control.get_text() == "Select"

    def test_select(self, control):
        """Test select() method."""
        control.select("Option2")
        assert control.get_text() == "Option2"


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestDynamicDropdown:
    """
    Test DynamicDropdown object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.dropdown_dynamic  # pylint: disable=no-member

    def test_get_text(self, control):
        """Test get_text() method."""
        assert control.get_text() == "Type to Select Countries"

    def test_select(self, control):
        """Test select() method."""
        control.select("Poland")
        assert control.get_text() == "Poland"

    def test_select_by_partial_value(self, control):
        """Test select_by_partial_value() method."""
        control.select_by_partial_value("Greece", 3)
        assert control.get_text() == "Greece"


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestLabel:
    """
    Test Label object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.table_fixed_label  # pylint: disable=no-member

    def test_get_text(self, control):
        """Test get_text() method."""
        assert control.get_text() == "Total Amount Collected: 296"


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestLink:
    """
    Test Link object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.blinking_text_link  # pylint: disable=no-member

    def test_get_text(self, control):
        """Test get_text() method."""
        assert control.get_text() == "Free Access to InterviewQues/ResumeAssistance/Material"

    def test_get_href(self, control):
        """Test get_href() method."""
        assert control.get_href() == "https://rahulshettyacademy.com/documents-request"


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestIFrame:
    """
    Test IFrame object.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.iframe  # pylint: disable=no-member

    def test_iframe_context_manager(self, control):
        """Test IFrame context manager."""
        with control as ctrl:
            assert ctrl.courses_link.get_href() == "https://courses.rahulshettyacademy.com/courses"


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestTableSimple:
    """
    Test Table object with SimpleTableStrategy.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return Table(self.driver, (By.NAME, "dummy_locator"), SimpleTableStrategy)  # pylint: disable=no-member

    @pytest.mark.skip(reason="not implemented")
    def test_get_headers(self, control):
        """Test get_headers() method."""
        assert control.get_headers() is None

    @pytest.mark.skip(reason="not implemented")
    def test_get_body(self, control):
        """Test get_body() method."""
        assert control.get_body() == []

    @pytest.mark.skip(reason="not implemented")
    def test_get_table(self, control):
        """Test get_table() method."""
        assert control.get_table() == []


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestTableWithHeadings:
    """
    Test Table object with HeadingsTableStrategy.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.table_static  # pylint: disable=no-member

    def test_get_headers(self, control):
        """Test get_headers() method."""
        assert control.get_headers() == ["Instructor", "Course", "Price"]

    def test_get_body(self, control):
        """Test get_body() method."""
        assert control.get_body() == [
            ["Rahul Shetty", "Selenium Webdriver with Java Basics + Advanced + Interview Guide", "30"],
            ["Rahul Shetty", "Learn SQL in Practical + Database Testing from Scratch", "25"],
            ["Rahul Shetty", "Appium (Selenium) - Mobile Automation Testing from Scratch", "30"],
            ["Rahul Shetty", "WebSecurity Testing for Beginners-QA knowledge to next level", "20"],
            ["Rahul Shetty", "Learn JMETER from Scratch - (Performance + Load) Testing Tool", "25"],
            ["Rahul Shetty", "WebServices / REST API Testing with SoapUI", "35"],
            ["Rahul Shetty", "QA Expert Course :Software Testing + Bugzilla + SQL + Agile", "25"],
            ["Rahul Shetty", "Master Selenium Automation in simple Python Language", "25"],
            ["Rahul Shetty", "Advanced Selenium Framework Pageobject, TestNG, Maven, Jenkins,C", "20"],
            ["Rahul Shetty", "Write effective QA Resume that will turn to interview call", "0"],
        ]

    def test_get_table(self, control):
        """Test get_table() method."""
        assert control.get_table() == [
            ["Instructor", "Course", "Price"],
            ["Rahul Shetty", "Selenium Webdriver with Java Basics + Advanced + Interview Guide", "30"],
            ["Rahul Shetty", "Learn SQL in Practical + Database Testing from Scratch", "25"],
            ["Rahul Shetty", "Appium (Selenium) - Mobile Automation Testing from Scratch", "30"],
            ["Rahul Shetty", "WebSecurity Testing for Beginners-QA knowledge to next level", "20"],
            ["Rahul Shetty", "Learn JMETER from Scratch - (Performance + Load) Testing Tool", "25"],
            ["Rahul Shetty", "WebServices / REST API Testing with SoapUI", "35"],
            ["Rahul Shetty", "QA Expert Course :Software Testing + Bugzilla + SQL + Agile", "25"],
            ["Rahul Shetty", "Master Selenium Automation in simple Python Language", "25"],
            ["Rahul Shetty", "Advanced Selenium Framework Pageobject, TestNG, Maven, Jenkins,C", "20"],
            ["Rahul Shetty", "Write effective QA Resume that will turn to interview call", "0"],
        ]


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestTableWithHeaderAndBody:
    """
    Test Table object with HeaderBodyTableStrategy.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return self.page.table_fixed_header  # pylint: disable=no-member

    def test_get_headers(self, control):
        """Test get_headers() method."""
        assert control.get_headers() == ["Name", "Position", "City", "Amount"]

    def test_get_body(self, control):
        """Test get_body() method."""
        assert control.get_body() == [
            ["Alex", "Engineer", "Chennai", "28"],
            ["Ben", "Mechanic", "Bengaluru", "23"],
            ["Dwayne", "Manager", "Kolkata", "48"],
            ["Ivory", "Receptionist", "Chennai", "18"],
            ["Jack", "Engineer", "Pune", "32"],
            ["Joe", "Postman", "Chennai", "46"],
            ["Raymond", "Businessman", "Mumbai", "37"],
            ["Ronaldo", "Sportsman", "Chennai", "31"],
            ["Smith", "Cricketer", "Delhi", "33"],
        ]

    def test_get_table(self, control):
        """Test get_table() method."""
        assert control.get_table() == [
            ["Name", "Position", "City", "Amount"],
            ["Alex", "Engineer", "Chennai", "28"],
            ["Ben", "Mechanic", "Bengaluru", "23"],
            ["Dwayne", "Manager", "Kolkata", "48"],
            ["Ivory", "Receptionist", "Chennai", "18"],
            ["Jack", "Engineer", "Pune", "32"],
            ["Joe", "Postman", "Chennai", "46"],
            ["Raymond", "Businessman", "Mumbai", "37"],
            ["Ronaldo", "Sportsman", "Chennai", "31"],
            ["Smith", "Cricketer", "Delhi", "33"],
        ]


@pytest.mark.unit
@pytest.mark.usefixtures("class_fixture")
class TestTableMixed:
    """
    Test Table object with MixedTableStrategy.
    """

    @pytest.fixture
    def control(self):
        """Setup object-under-test."""
        return Table(self.driver, (By.NAME, "dummy_locator"), MixedTableStrategy)  # pylint: disable=no-member

    @pytest.mark.skip(reason="not implemented")
    def test_get_headers(self, control):
        """Test get_headers() method."""
        assert control.get_headers() == []

    @pytest.mark.skip(reason="not implemented")
    def test_get_body(self, control):
        """Test get_body() method."""
        assert control.get_body() == []

    @pytest.mark.skip(reason="not implemented")
    def test_get_table(self, control):
        """Test get_table() method."""
        assert control.get_table() == []
