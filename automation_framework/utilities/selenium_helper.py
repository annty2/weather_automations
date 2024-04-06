import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class SeleniumHelper:
    def simulate_typing(self, element: WebElement, text: str, delay: float = 0) -> None:
        # Types text into a web element, character by character, with an optional delay
        for char in text:
            element.send_keys(char)  # Sends each character to the element
            time.sleep(delay)  # Waits between each keystroke

    def wait_for_element(self, driver: WebDriver, selector: str, wait_time: int = 5) -> WebElement:
        # Waits for a specific element to be present in the DOM
        return WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )  # Waits for the element using CSS selector

    def click_element_with_js(self, driver: WebDriver, selector: str):
        # Clicks on an element using JavaScript
        driver.execute_script(f"document.querySelector(`{selector}`).click()")
        # Executes a JavaScript command to click the element
