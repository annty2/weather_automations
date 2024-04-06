import requests
from automation_framework import config
from automation_framework.utilities.exeptions import CityNotFound


class ApiHelper:
    _BASE_URL = config.BASE_URL
    _API_KEY = config.API_KEY
    _UNIT = "metric"
    _LANG = "en"

    def get_current_weather(self, city: str):
        # Construct the URL to fetch current weather for a city
        url = f"{self._BASE_URL}?q={city}&appid={self._API_KEY}&units={self._UNIT}&lang={self._LANG}"
        response = requests.get(url)  # Make the API request

        # Raise an exception if the city is not found
        if response.status_code == 404:
            raise CityNotFound(f"Searching for {city} in the API responded with: {response.status_code}")

        return response.json()  # Return the JSON response if successful

    def get_current_weather_by_city_id(self, city_id: str):
        # Construct the URL to fetch current weather using a city ID
        url = f"{self._BASE_URL}?id={city_id}&appid={self._API_KEY}&units={self._UNIT}&lang={self._LANG}"
        response = requests.get(url)  # Make the API request
        return response  # Return the response object
