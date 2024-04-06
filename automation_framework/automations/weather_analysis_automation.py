from automation_framework.automations.base_selenium_automation import BaseSeleniumAutomation
from automation_framework.city_reporter.city_reporter import CityReporter, Status
from automation_framework.pages.weather_page import WeatherPage
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.cities_api_helpers import CitiesApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from automation_framework.utilities.exeptions import CityNotFound


class WeatherAnalysisAutomation(BaseSeleniumAutomation):
    """Class to automate weather analysis."""

    _BLANK_CELL = 'N/A'  # Placeholder for missing data
    _city_api = CitiesApiHelper()  # API helper for city name retriever API
    _weather_api = ApiHelper()  # API helper for weather retriever API

    def run(self):
        """Executes the automation workflow."""
        database = DatabaseHelper()
        city_reporter = CityReporter()

        # Retrieve a list of countries and their corresponding cities
        list_country_city = self._city_api.get_counties_and_cities()

        for item in list_country_city:
            city = self._format_city_name(item)
            country = item['country']
            weather_page = WeatherPage(self.driver)

            # Get temperature from the web interface
            temperature_web = weather_page.get_city_temperature(city, country)

            # Fetch current weather data from the API
            try:
                data = self._weather_api.get_current_weather(city)
            except CityNotFound:
                # Report if city is not found in the API
                city_reporter.append_to_report(city, self._BLANK_CELL, str(temperature_web), self._BLANK_CELL,
                                               Status.API_NOT_FOUND)
                continue

            # Extract feels like and temperature from API data
            feels_like_api, temperature_api = self._get_temperature_and_feels_like_from_response(data)

            # Store the weather data in the database
            self._insert_city_temperature_feels_like_into_db(database, city, temperature_api, feels_like_api)

            # Retrieve the stored weather data for comparison
            db_result = database.get_weather_data(city)
            temperature_db = db_result[1]

            # Calculate and report the temperature difference
            if temperature_web is not None:
                temperature_difference = str(temperature_db - temperature_web)
                city_reporter.append_to_report(city, temperature_api, str(temperature_web), temperature_difference,
                                               Status.SUCCESS)
            else:
                # Report if temperature is not found on the website
                city_reporter.append_to_report(city, str(temperature_db), self._BLANK_CELL, self._BLANK_CELL,
                                               Status.WEB_NOT_FOUND)

        # Save the report
        city_reporter.save_report()

        # Close the browser session
        self.driver.quit()

    def _get_temperature_and_feels_like_from_response(self, data: dict):
        """Extracts temperature and feels like from API response."""
        return data['main']['feels_like'], data['main']['temp']

    def _insert_city_temperature_feels_like_into_db(self, db: DatabaseHelper, city, temperature, feels_like):
        """Inserts temperature data into the database."""
        db.insert_weather_data(city, temperature, feels_like)

    def _format_city_name(self, item: dict):
        """Formats city names to remove any single quotes."""
        return str(item['city']).replace("'", "")


if __name__ == "__main__":
    WeatherAnalysisAutomation().run()  # Run the automation
