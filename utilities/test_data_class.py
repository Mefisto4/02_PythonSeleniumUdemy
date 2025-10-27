"""
Contains TestData class.
"""

from typing import Any, Dict


class TestDataClass:
    """
    Class for easier usage of test data provided by JSON. Instance's attributes
    correspond with test data keys and attributes' values correspond with
    test data values, i.e.:

    test_data_set: Dict =   {
                              "product_name": "Blackberry",
                              "delivery_country": "Poland",
                              "type_len": 2
                            }

    test_data_instance: TestDataClass =
                    TestDataClass(test_data_set.keys(), test_data_set.values())

        >> test_data_instance.product_name
        >> 'Blackberry'
    """

    def __init__(self, data: Dict[str, Any]):
        """

        :param data: dict of test data from JSON
        """
        self._data = data
        for key, value in zip(self._data.keys(), self._data.values()):
            self.__dict__[key] = value

    def get_data(self) -> Dict[str, Any]:
        """
        Returns test data.

        :return: dict of test data
        """
        return self._data

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Sets new test data.

        :param data: dict of test data
        :return: None
        """
        keys = self._data.keys()
        for key in keys:
            del self.__dict__[key]

        for key, value in zip(data.keys(), data.values()):
            self.__dict__[key] = value
