from time import sleep
from typing import Optional

from selenium.webdriver.common.by import By

from automation_framework.pages.base_page import BasePage
from automation_framework.utilities.exeptions import ElementNotFound


class WeatherPage(BasePage):
    # Selectors for various elements on the weather page
    _WEATHER_PAGE_LOADED_SELECTOR = 'table.zebra'
    _CITY_PAGE_LOADED_SELECTOR = '#qlook'
    _SEARCH_BOX_SELECTOR = "input.picker-city__input[type='search']"
    _AUTOCOMPLETE_LIST_ITEM_SELECTOR = '.asu li a'
    _TEMPERATURE_ELEMENT_SELECTOR = '#cur-weather + .h2'

    _CELSIUS = '°C'  # Unit of temperature

    @property
    def _url(self):
        # Property to get the URL of the weather page
        return f"{super()._url}/weather/"

    def go_to_weather_page(self):
        # Navigates to the weather page and waits for it to load
        super().go_to_page()
        self._selenium_helper.wait_for_element(self.driver, selector=self._WEATHER_PAGE_LOADED_SELECTOR)

    def get_temperature_from_city_page(self) -> float:
        # Retrieves temperature from the city-specific weather page
        try:
            self._selenium_helper.wait_for_element(self.driver, selector=self._CITY_PAGE_LOADED_SELECTOR)
        except Exception:
            raise ElementNotFound("City page did not load")

        element = self.driver.find_element(By.CSS_SELECTOR, self._TEMPERATURE_ELEMENT_SELECTOR)
        temperature = element.text.replace(self._CELSIUS, '').strip()
        try:
            return float(temperature)
        except ValueError:
            raise ValueError(f"Temperature value is {temperature}. It's not a number.")

    def search_for_city_country(self, city: str, country: str):
        # Performs a search for a city and country on the weather page
        search_box = self.driver.find_element(By.CSS_SELECTOR, self._SEARCH_BOX_SELECTOR)
        text_to_search = f"{city} {country}"
        self._selenium_helper.simulate_typing(search_box, text_to_search)
        sleep(1)  # Wait for autocomplete suggestions to appear
        try:
            self._selenium_helper.click_element_with_js(self.driver, self._AUTOCOMPLETE_LIST_ITEM_SELECTOR)
        except Exception as e:
            print(e)

    def get_city_temperature(self, city: str, country: str) -> Optional[float]:
        # Fetches the temperature for a given city
        self.go_to_weather_page()
        self.search_for_city_country(city, country)
        try:
            return self.get_temperature_from_city_page()
        except Exception as e:
            print(e)
            return None
