from typing import List, Tuple

import pytest
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper


class TestWeatherData:

    @pytest.fixture(scope="module")
    def api(self):
        return ApiHelper()

    @pytest.fixture
    def database(self):
        return DatabaseHelper()

    @pytest.mark.parametrize("city", ["Haifa", "Ashdod", "New York"])
    def test_get_weather_data(self, api: ApiHelper, database: DatabaseHelper, city: str):
        # Get temperature and feels like from the API
        feels_like_api, temperature_api = self._get_temperature_and_feels_like_from_api(api, city)

        # Insert city, temperature and feels like to the DB
        self._insert_city_temperature_feels_like_into_db(database, city, temperature_api, feels_like_api)

        # Get from the DB the temperature and feels like
        _, temperature_db, feels_like_db = database.get_weather_data(city)

        # Test if api data and what actually saved in DB are equal
        assert temperature_api == temperature_db
        assert feels_like_api == feels_like_db

    @pytest.mark.parametrize("city_ids", [["294801", "295629", "5128581"]])
    def test_utilize_weather_data_multiple_cities(self, api: ApiHelper, database: DatabaseHelper, city_ids: List[str]):
        # Add new column to the DB
        database.add_column("average_temperature", "REAL")

        for city_id in city_ids:
            # Get city name from API by city ID
            data = self._get_current_weather_by_city_id(api, city_id)

            city_name = data['name']

            # Get temperature and feels_like from API by city name
            feels_like_api, temperature_api = self._get_temperature_and_feels_like_from_api(api, city_name)

            # Insert into DB city, temperature and feels like
            self._insert_city_temperature_feels_like_into_db(database, city_name, temperature_api, feels_like_api)

            # Calculate average temperature by max and min temperatures
            avg_temperature_api = self._calculate_average_temperature(data)

            # Update city in DB with the average temperature
            database.update_avg_temp_in_db(avg_temperature_api, city_name)

            # Get from the DB the temperature and feels like
            _, temperature_db, feels_like_db, avg_temperature_db = database.get_weather_data(city_name)

            # Test if api data and what actually saved in DB are equal
            assert temperature_api == temperature_db
            assert feels_like_api == feels_like_db
            assert avg_temperature_api == avg_temperature_db

        self._print_max_average_temperature_city(database)

    def _get_current_weather_by_city_id(self, api: ApiHelper, city_id: str):
        id_response = api.get_current_weather_by_city_id(city_id)

        assert id_response.status_code == 200

        return id_response.json()

    def _get_temperature_and_feels_like_from_response(self, data: dict) -> Tuple[float, float]:
        feels_like = data['main']['feels_like']
        temperature = data['main']['temp']

        return feels_like, temperature

    def _insert_city_temperature_feels_like_into_db(self, db: DatabaseHelper, city, temperature, feels_like):
        db.insert_weather_data(city, temperature, feels_like)

    def _get_temperature_and_feels_like_from_api(self, api: ApiHelper, city: str):
        data = api.get_current_weather(city)

        return self._get_temperature_and_feels_like_from_response(data)

    def _calculate_average_temperature(self, data: dict) -> float:
        data_min = data['main']['temp_min']
        data_max = data['main']['temp_max']

        return round((data_min + data_max) / 2, 2)

    def _print_max_average_temperature_city(self, database: DatabaseHelper):
        max_avg_temperature_city = database.get_highest_temp_avg_city()[0]

        print(max_avg_temperature_city)
