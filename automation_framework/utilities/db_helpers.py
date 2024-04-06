import sqlite3

from automation_framework import config
from automation_framework.sql_quries import SQLQuery
from automation_framework.utilities.exeptions import EntryNotFound


class DatabaseHelper:
    def __init__(self, db_name=config.DB_NAME):
        self.conn = sqlite3.connect(db_name)  # Initialize a SQLite database connection
        self._create_tables()  # Create table

    def _create_tables(self):
        with self.conn:  # Create tables if they don't exist
            query = SQLQuery('create_weather_data_table.sql').read()
            self.conn.execute(query)

    def insert_weather_data(self, insert_city: str, insert_temperature: float, insert_feels_like: float):
        with self.conn:  # Insert weather data into the database
            try:
                query = SQLQuery('insert_city_temp_feels_like.sql').read(insert_city=insert_city,
                                                                         insert_temperature=insert_temperature,
                                                                         insert_feels_like=insert_feels_like)
                self.conn.execute(query)
            except Exception as e:
                print(e)  # Print the error if insertion fails

    def get_weather_data(self, city: str):
        # Retrieve weather data for a specific city
        query = SQLQuery('select_weather_data_by_city.sql').read(city=city)
        result = self.conn.execute(query).fetchone()
        if result is None:
            raise EntryNotFound(f"{city} not found in table weather_data")  # Raise an exception if the city is not found

        return result  # Return the retrieved result

    def add_column(self, column_name: str, column_type: str):
        try:
            with self.conn:  # Add a new column to the weather_data table
                query = SQLQuery('add_average_temp_column.sql').read(column_name=column_name,
                                                                         column_type=column_type)
                self.conn.execute(query)
        except Exception as e:
            print(f"Error occurred: {e}")  # Print the error if the operation fails

    def update_avg_temp_in_db(self, avg_temp: float, city: str):
        try:
            with self.conn:  # Update the average temperature for a city
                query = SQLQuery('update_avg_temp_in_table.sql').read(avg_temp=avg_temp,
                                                                         city=city)
                self.conn.execute(query)
        except Exception as e:
            print(f"Error occurred: {e}")  # Print the error if the update fails

    def get_highest_temp_avg_city(self):
        # Retrieve the city with the highest average temperature
        try:
            with self.conn:
                query = SQLQuery('select_city_by_max_avg_temp.sql').read()
                result = self.conn.execute(query).fetchone()
        except Exception as e:
            print(f"Error occurred: {e}")  # Print the error if the query fails

        return result  # Return the city if found
