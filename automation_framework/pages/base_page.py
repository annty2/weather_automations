from abc import ABC
from selenium.webdriver.chrome.webdriver import WebDriver
from automation_framework.utilities.selenium_helper import SeleniumHelper

class BasePage(ABC):
    # Shared SeleniumHelper instance for all page objects
    _selenium_helper = SeleniumHelper()

    def __init__(self, driver: WebDriver):
        # Initialize the page with a WebDriver instance
        self.driver = driver

    @property
    def _url(self):
        # Base URL for the pages, can be overridden by subclasses
        return "https://www.timeanddate.com"

    def go_to_page(self):
        # Navigate to the page's URL using the WebDriver
        self.driver.get(self._url)
