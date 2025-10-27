"""
End-to-end tests of Angular Practice Shop page.
"""

import json
from typing import Any, Dict

import pytest
from selenium.common import NoSuchElementException

from pages.rsa_pages.angular_practice_shop_page import AngularPracticeShopPage
from utilities.test_data_class import TestDataClass

TEST_DATA_PATH = "./test_data/test_angular_practice_shop_e2e.json"
with open(file=TEST_DATA_PATH, encoding="utf-8") as json_file:
    data = json.load(json_file)


@pytest.fixture(scope="class")
def class_fixture(request, test_fixture):
    """
    Setup test specific fixture.
    """
    request.cls.tools = test_fixture
    request.cls.driver = request.cls.tools.driver
    request.cls.page = AngularPracticeShopPage(request.cls.driver)


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("order_basic"), scope="class")
class TestAngularPracticeShopOrderBasic:
    """
    Test basic order scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: TestDataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return TestDataClass(test_data_set)

    def test_add_product_to_cart(self, test_data):
        """Test if product is added to cart."""
        self.page.go_to()
        self.page.add_product_to_cart(test_data.product_name)

        assert self.page.get_number_of_products_in_cart() == test_data.product_quantity

    def test_checkout_view(self, test_data):
        """Test if checkout view shows correct information."""
        checkout_view = self.page.go_to_checkout()

        product = checkout_view.get_products()[0]

        assert product.name == test_data.product_name
        assert product.quantity == test_data.product_quantity
        assert product.price == test_data.product_price
        assert product.total == test_data.product_price
        assert checkout_view.get_total_price() == test_data.product_price

    def test_delivery_view(self, test_data):
        """Test if delivery location can be chosen."""
        delivery_view = self.page.checkout_view.go_to_delivery()
        if test_data.type_len < 0:
            delivery_view.delivery_location_dropdown.select(test_data.delivery_country)
        else:
            delivery_view.delivery_location_dropdown.select_by_partial_value(
                test_data.delivery_country, test_data.type_len
            )

        assert delivery_view.delivery_location_dropdown.get_text() == test_data.delivery_country

    def test_purchase_view(self, test_data):
        """Test if purchase can be done successfully."""
        self.page.delivery_view.terms_and_conditions_checkbox.select()
        self.page.delivery_view.purchase_button.click()
        assert self.page.delivery_view.alert_message_label.is_displayed()
        assert test_data.success_msg in self.page.delivery_view.alert_message_label.get_text()
        self.page.delivery_view.alert_message_close_button.click()
        with pytest.raises(NoSuchElementException):
            assert not self.page.delivery_view.alert_message_label.is_displayed()


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("order_with_changes"), scope="class")
class TestAngularPracticeShopOrderWithChanges:
    """
    Test order with products quantities changes scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: TestDataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return TestDataClass(test_data_set)

    def _verify_cart(self, expected_data: Dict[str, Any]):
        products = self.page.checkout_view.get_products()  # type: ignore[attr-defined]
        total = 0.0
        for product in products:
            assert product.name in expected_data.keys()
            assert product.quantity == expected_data[product.name][0]
            assert product.price == expected_data[product.name][1]
            assert product.total == expected_data[product.name][0] * expected_data[product.name][1]
            total += product.total
        assert total == self.page.checkout_view.get_total_price()  # type: ignore[attr-defined]

    def _modify_quantity(self, new_data: Dict[str, Any]):
        products = self.page.checkout_view.get_products()  # type: ignore[attr-defined]
        for i in products:
            if i.name in new_data.keys():
                i.change_quantity(new_data[i.name][0])

    def test_add_products_to_cart(self, test_data):
        """Test if multiple products can be added to cart."""
        self.page.go_to()
        for product in test_data.products.keys():
            self.page.add_product_to_cart(product)

        assert self.page.get_number_of_products_in_cart() == len(test_data.products.keys())

    def test_checkout_view_initial(self, test_data):
        """Test if checkout view shows correct information."""
        checkout_view = self.page.go_to_checkout()

        products = checkout_view.get_products()
        assert len(products) == len(test_data.products.keys())

        expected_data = test_data.products
        self._verify_cart(expected_data)

    def test_checkout_view_add_product(self, test_data):
        """Test if the product quantity can be increased."""
        self._modify_quantity(test_data.product_more)

        expected_data = test_data.products
        expected_data.update(test_data.product_more)

        self._verify_cart(expected_data)

    def test_checkout_view_zero_product(self, test_data):
        """Test if the product quantity can be equal to 0."""
        self._modify_quantity(test_data.product_zero)

        expected_data = test_data.products
        expected_data.update(test_data.product_more)
        expected_data.update(test_data.product_zero)

        self._verify_cart(expected_data)

    def test_checkout_view_fraction_product(self, test_data):
        """Test if the product quantity cannot be fractional."""
        self._modify_quantity(test_data.product_fraction)

        products = self.page.checkout_view.get_products()
        for i in products:
            if i.name in test_data.product_fraction.keys():
                assert i.quantity.is_integer(), "Quantity of a product must be an integer."

    def test_checkout_view_negative_product(self, test_data):
        """Test if the product quantity cannot be negative."""
        self._modify_quantity(test_data.product_minus)

        products = self.page.checkout_view.get_products()
        for i in products:
            if i.name in test_data.product_minus.keys():
                assert i.quantity >= 0, "Quantity of a product cannot be negative."

    def test_checkout_view_continue_shopping(self):
        """Test if 'Continue Shopping' button navigates back to shop page with cart content intact."""
        self.page.checkout_view.continue_shopping_button.click()

        assert self.page.get_number_of_products_in_cart() > 0, "Cart should not get reset."


@pytest.mark.e2e
@pytest.mark.usefixtures("class_fixture")
@pytest.mark.parametrize("test_data_set", data.get("order_with_removals"), scope="class")
class TestAngularPracticeShopOrderWithRemovals:
    """
    Test order with products removal scenario.
    """

    # pylint: disable=no-member

    @pytest.fixture
    def test_data(self, test_data_set):
        """
        Test data fixture.

        :param test_data_set: dict
        :return: TestDataClass()
                        .product_name
                        .delivery_country
                        .type_len
        """
        return TestDataClass(test_data_set)

    def test_add_products_to_cart(self, test_data):
        """Test if multiple products can be added to cart."""
        self.page.go_to()
        for product in test_data.products:
            self.page.add_product_to_cart(product)

        assert self.page.get_number_of_products_in_cart() == len(test_data.products)

    def test_checkout_view_initial(self, test_data):
        """Test if checkout view shows correct information."""
        checkout_view = self.page.go_to_checkout()
        products = checkout_view.get_products()

        assert len(products) == len(test_data.products)

    def test_checkout_view_remove_products(self, test_data):
        """Test if the products can be removed from cart."""
        products = self.page.checkout_view.get_products()
        for product in products:
            product.remove()

        assert self.page.checkout_view.get_total_price() == test_data.total_final

    def test_checkout_view_proceed(self):
        """Test if user cannot proceed to delivery with empty cart."""
        assert not self.page.checkout_view.checkout_button.is_enabled(), "Checkout button should be inactive."
