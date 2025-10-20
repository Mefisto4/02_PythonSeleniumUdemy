"""
Configuration file for pytest fixtures.
"""

import logging
from logging import Logger
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def pytest_addoption(parser) -> None:
    """
    Add command line options to pytest.

    :param parser: parser for command line arguments and ini-file values.
    :return: None
    """
    parser.addoption(
        "--browser-name",
        action="store",
        default="chrome",
        help="browser selection: chrome, firefox, safari, edge",
    )


class TestTools:
    """
    Class that contains objects necessary for testing.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.driver: WebDriver | None = None
        self.logger: Logger | None = None
        self.wait: WebDriverWait | None = None
        self.ec = expected_conditions


@pytest.fixture(scope="session")
def test_tools() -> TestTools:
    """
    Fixture for getting TestTools object.

    :return: TestTools()
    """
    tools = TestTools()
    return tools


@pytest.fixture(scope="session")
def logging_tool(test_tools) -> Generator[TestTools]:  # pylint: disable=redefined-outer-name
    """
    Fixture for setting up and starting logger.

    :param test_tools: TestTools()
    :return: TestTools()
    """
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler("reports/console-logs.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    test_tools.logger = logger

    test_tools.logger.info("Logging started.")
    yield test_tools
    test_tools.logger.info("Logging ended.")


@pytest.fixture(scope="class")
def browser_instance(request, logging_tool) -> Generator[TestTools]:  # pylint: disable=redefined-outer-name
    """
    Fixture for getting WebDriver instance based on browser selection by user's command line input, i.e.:
        >> pytest --browser-name firefox

    :param request: the ``request`` fixture (see: class FixtureRequest in Selenium)
    :param logging_tool: TestTools()
    :return: TestTools()
    """
    tools = logging_tool

    browser_name = request.config.getoption("--browser-name")
    tools.logger.info(f"Browser name: {browser_name}.")

    if browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "safari":
        driver = webdriver.Safari()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:  # default option is "chrome"
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.password_manager_leak_detection": False,
            "excludeSwitches": ["enable-logging"],
        }
        tools.logger.info(f"Custom browser preferences: {prefs}.")
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.implicitly_wait(5)

    tools.driver = driver
    tools.logger.info(f"WebDriver created - instance: {driver.name}.")
    yield tools
    tools.driver.quit()
    tools.logger.info("WebDriver quitted.")


@pytest.fixture(scope="class")
def web_driver_wait(browser_instance) -> Generator[TestTools]:  # pylint: disable=redefined-outer-name
    """
    Fixture for setting up explicit wait.

    :param browser_instance: TestTools()
    :return: TestTools()
    """
    tools = browser_instance

    wait_s = 10
    tools.wait = WebDriverWait(tools.driver, wait_s)

    tools.logger.info(f"Added WebDriver wait: {wait_s}[s].")
    yield tools


@pytest.fixture(scope="class")
def test_fixture(web_driver_wait) -> Generator[TestTools]:  # pylint: disable=redefined-outer-name
    """
    Final fixture as a wrapper before testing.

    :param web_driver_wait: TestTools()
    :return: TestTools()
    """
    tools = web_driver_wait

    tools.logger.info("Testing started.")
    yield tools
    tools.logger.info("Testing finished.")
