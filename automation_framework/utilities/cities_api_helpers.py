from typing import List
import requests

class CitiesApiHelper:
    # Base URL for the REST Countries API and a tuple of locations to skip
    _BASE_URL = "https://restcountries.com/v3.1"
    _SKIPS = ('Norfolk Island',) # List of countries to skip

    def get_counties_and_cities(self):
        # Fetches countries and their capital cities
        url = f"{self._BASE_URL}/all?fields=capital,name"
        response = requests.get(url)  # Perform the API request
        data = response.json()  # Convert the response to JSON

        return self._format_cities(data)  # Format and return the cities data

    def _format_cities(self, data: List[dict]):
        # Formats the API response to extract and return relevant city and country information
        result = []  # Initialize an empty list for results
        for country in data:  # Iterate through each country in the data
            country_name = country['name']['common']  # Extract the country name
            if country_name in self._SKIPS:  # Skip the country if it's in the _SKIPS list
                continue

            capitals = country['capital']  # Get the list of capitals
            if len(capitals) == 0:  # Continue if there are no capitals
                continue

            # Append the country and its capital to the results list
            result.append({
                "country": country_name,
                "city": capitals[0],  # Take the first capital if there are multiple
            })

        return result  # Return the formatted list of countries and cities
