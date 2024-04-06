# Weather Automations and Tests

## Description

This project focuses on testing and automating weather-related functionalities. It adheres to specific instructions outlined in `questions.text`, providing a structured and detailed approach to weather data manipulation and analysis.

## Requirements

- Python 3.10
- SQLite
- Selenium WebDriver

## Structure

- 📁 `weather_analysis_automation/automations` - Contains scripts for weather automations.
- 📁 `weather_analysis_automation/tests` - Includes tests for weather-related functionalities.
- 📁 `weather_analysis_automation/utilities` - Various helper scripts for database operations and API interactions.
- 📁 `weather_analysis_automation/sql_queries` - Stores different SQL queries and includes a utility to convert them into executable statements.
- 📁 `weather_analysis_automation/pages` - Page classes for automations, facilitating page object model usage.
- 📄 `weather_analysis_automation/config.py` - Script to pull configurations from `config/config.ini`.
- 📄 `requirements.txt` - Lists all the necessary Python packages for the project.

## Installation

To set up the environment for the project, you can install all the required packages using:

```
pip install -r requirements.txt
```

Alternatively, you can install the required packages individually using:

```
pip install [package_name]
```

Ensure that `requests` and `pytest` are included in your installations.

## Running the Tests and Automations
Note: Insert your `API_KEY` to the `config/config.ini` file

- **Task 1 & 2:** To run the tests related to the OpenWeather API, execute the following command:
- **Task 4:** To run the weather analysis automation script, use:
