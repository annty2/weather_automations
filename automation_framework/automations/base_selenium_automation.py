from abc import ABC, abstractmethod

from selenium import webdriver


class BaseSeleniumAutomation(ABC):
    def __init__(self):
        self.driver = self._get_webdriver()

    def _get_webdriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.page_load_strategy = 'eager'

        web_driver = webdriver.Chrome(options=options)

        return web_driver

    @abstractmethod
    def run(self):
        pass
