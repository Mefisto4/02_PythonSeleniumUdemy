"""
Contains AngularPracticeShop page objects.
"""

from __future__ import annotations

from typing import List

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.rsa_pages import PROTO_COMMERCE_SHOP_PAGE
from utilities.control_objects.button import Button
from utilities.control_objects.checkbox_radiobutton import Checkbox
from utilities.control_objects.dropdown import DropdownDynamic
from utilities.control_objects.label import Label


class _AngularPracticeShopPage(BasePage):
    """
    Base page class for AngularPracticeShop pages.
    """

    URL = PROTO_COMMERCE_SHOP_PAGE

    def __init__(self, driver: WebDriver, url=URL) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        :param url: URL of webpage, i.e.: "https://www.google.com"
        """
        super().__init__(driver, url)


class AngularPracticeShopPage(_AngularPracticeShopPage):
    """
    Web page for angular practice shop (ProtoCommerce).
    """

    def __init__(self, driver: WebDriver) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        """
        super().__init__(driver)
        self._locators = _AngularPracticeShopPageLocators

    @property
    def checkout_button(self) -> Button:
        """
        Returns checkout button.

        :return: Button
        """
        return Button(self.driver, self._locators.CHECKOUT_BUTTON)

    @property
    def checkout_view(self) -> CheckoutViewPage:
        """
        Returns checkout view page object.

        :return: CheckoutViewPage object.
        """
        return CheckoutViewPage(self.driver)

    @property
    def delivery_view(self) -> DeliveryLocationViewPage:
        """
        Returns delivery view page object.

        :return: DeliveryLocationViewPage object.
        """
        return DeliveryLocationViewPage(self.driver)

    def add_product_to_cart(self, product_name: str) -> None:
        """
        Looks for the product name and adds it to the cart using locator chaining method.

        Alternatively to locator chaining method, the DOM traversing method could be used with only 1 locator:
            >> driver.find_element(
                    By.XPATH,
                    (f"//h4[@class='card-title']/a[text()='{"
                    f"product_name}']/parent::h4/parent::div/parent::div/div/button["
                    f"@class='btn btn-info']")
                ).click()

        :param product_name: product available on the page to be added to the cart
        :return: None
        """
        for product in self.driver.find_elements(By.XPATH, "//div[@class='card h-100']"):
            name = product.find_element(By.XPATH, "div/h4/a").text
            if name == product_name:
                product.find_element(By.XPATH, "div/button").click()
                break

    def get_number_of_products_in_cart(self) -> int:
        """
        Extract number of products in the cart from text of the button element.
        Text example: " Checkout ( 1 )\n"

        :return: number of products in the cart.
        """
        amount = self.checkout_button.web_element.text
        return int(amount.split("(")[1].split(")")[0].strip(" "))

    def go_to_checkout(self) -> CheckoutViewPage:
        """
        Goes to Checkout view by clicking the checkout button.

        :return: CheckoutViewPage object.
        """
        self.checkout_button.click()
        return self.checkout_view


class _CheckoutProduct:
    """
    Represents product details from checkout view page table.
    """

    def __init__(self, web_element: WebElement) -> None:
        """

        :param web_element: web element of <tr>
        """
        self.web_element = web_element

    @property
    def name(self) -> str:
        """
        Returns product name.

        :return: str
        """
        return self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(1) .media-body h4 a").text

    @property
    def quantity(self) -> float:
        """
        Returns product quantity.

        :return: float
        """
        value = self.web_element.find_element(By.CSS_SELECTOR, "input[class='form-control']").get_attribute("value")
        if isinstance(value, str):
            return float(value)
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")

    @property
    def price(self) -> float:
        """
        Returns product price.

        :return: float
        """
        value = self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(3)").get_attribute("textContent")
        if isinstance(value, str):
            return float(value.split(" ")[1])
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")

    @property
    def total(self) -> float:
        """
        Returns product total price - should be equal to (quantity * price).

        :return: float
        """
        value = self.web_element.find_element(By.CSS_SELECTOR, "td:nth-child(4)").get_attribute("textContent")
        if isinstance(value, str):
            return float(value.split(" ")[1])
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")

    def remove(self) -> None:
        """
        Removes product from cart.

        :return: None
        """
        self.web_element.find_element(By.CSS_SELECTOR, "button[class='btn btn-danger']").click()

    def change_quantity(self, quantity: float) -> None:
        """
        Changes product quantity.

        :param quantity: quantity value to set
        :return: None
        """
        elem = self.web_element.find_element(By.CSS_SELECTOR, "input[class='form-control']")
        elem.clear()
        elem.send_keys(str(quantity))
        elem.send_keys(Keys.RETURN)

        if self.quantity != quantity:
            raise ValueError(f"Quantity did not change correctly. Got {self.quantity} instead of {quantity}.")


class CheckoutViewPage(_AngularPracticeShopPage):
    """
    Checkout view of AngularPracticeShopPage.
    """

    def __init__(self, driver: WebDriver) -> None:
        """

        :param driver: WebDriver for current browser, i.e.: webdriver.Chrome()
        """
        super().__init__(driver)
        self._locators = _CheckoutViewLocators

    @property
    def checkout_button(self) -> Button:
        """
        Returns checkout button.

        :return: Button
        """
        return Button(self.driver, self._locators.CHECKOUT_BUTTON)

    @property
    def continue_shopping_button(self) -> Button:
        """
        Returns 'Continue Shopping' button.

        :return: Button
        """
        return Button(self.driver, self._locators.CONTINUE_SHOPPING_BUTTON)

    def get_products(self) -> List[_CheckoutProduct]:
        """
        Returns list of the products from checkout view.
        :return: list of _CheckoutProduct
        """
        elems = self.driver.find_elements(By.XPATH, "//input[@class='form-control']/parent::td/parent::tr")
        return [_CheckoutProduct(elem) for elem in elems]

    def go_to_delivery(self) -> DeliveryLocationViewPage:
        """
        Goes to Delivery view by clicking the checkout button.

        :return: DeliveryLocationViewPage object.
        """
        self.checkout_button.click()
        return DeliveryLocationViewPage(self.driver)

    def get_total_price(self) -> float:
        """
        Returns cart total price - should be equal to sum of total prices of each product.

        :return: float
        """
        value = self.driver.find_element(By.CSS_SELECTOR, "td[class='text-right'] h3").get_attribute("textContent")
        if isinstance(value, str):
            return float(value.split(" ")[1])
        raise TypeError(f"Received unexpected value type:\n TYPE: {type(value)}\n EXPECTED: <class 'str'>\n")


class DeliveryLocationViewPage(_AngularPracticeShopPage):
    """
    Delivery location view of AngularPracticeShopPage.
    """

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self._locators = _DeliveryLocationViewPageLocators

    @property
    def delivery_location_dropdown(self) -> DropdownDynamic:
        """
        Returns delivery location dropdown.

        :return: DropdownDynamic
        """
        return DropdownDynamic(
            driver=self.driver,
            dropdown_locator=self._locators.DYNAMIC_DROPDOWN,
            dropdown_list_locator=self._locators.DROPDOWN_LIST,
            dropdown_list_item_locator=self._locators.DROPDOWN_LIST_ITEM,
        )

    @property
    def terms_and_conditions_checkbox(self) -> Checkbox:
        """
        Returns checkbox for terms and conditions.

        :return: Checkbox
        """
        return Checkbox(self.driver, self._locators.TERMS_AND_CONDITIONS_CHECKBOX)

    @property
    def purchase_button(self) -> Button:
        """
        Returns 'Purchase' button.

        :return: Button
        """
        return Button(self.driver, self._locators.PURCHASE_BUTTON)

    @property
    def alert_message_label(self) -> Label:
        """
        Returns purchase message label.

        :return: Label
        """
        return Label(self.driver, self._locators.ALERT_MESSAGE)

    @property
    def alert_message_close_button(self) -> Button:
        """
        Returns purchase message close button.

        :return: Button
        """
        return Button(self.driver, self._locators.ALERT_BUTTON)


class _AngularPracticeShopPageLocators:
    """
    Contains locators for AngularPracticeShopPage.
    """

    # pylint: disable=too-few-public-methods

    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a[class*='btn-primary']")


class _CheckoutViewLocators:
    """
    Contains locators for CheckoutViewPage.
    """

    # pylint: disable=too-few-public-methods

    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(@class,'btn-success')]")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//button[contains(@class,'btn-default')]")
    QUANTITY_TEXTBOX = (By.ID, "exampleInputEmail1")


class _DeliveryLocationViewPageLocators:
    """
    Contains locators for DeliveryLocationViewPage.
    """

    # pylint: disable=too-few-public-methods

    DYNAMIC_DROPDOWN = (By.ID, "country")
    DROPDOWN_LIST = (By.CSS_SELECTOR, "div[class='suggestions'] a")
    DROPDOWN_LIST_ITEM = (By.XPATH, "//a[text()='{}']")
    TERMS_AND_CONDITIONS_CHECKBOX = (By.CSS_SELECTOR, "div[class*='checkbox']")
    PURCHASE_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    ALERT_MESSAGE = (By.CLASS_NAME, "alert-success")
    ALERT_BUTTON = (By.CSS_SELECTOR, "a[data-dismiss='alert']")
