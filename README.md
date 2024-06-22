# PyWeather

    - PyWeather is a weather application built using Python and PyQt6. It fetches and displays current weather data and a 5-day forecast for a specified location using the OpenWeatherMap API.

## Features

    - Displays current weather conditions including temperature, humidity, wind speed, and visibility.
    - Provides a 5-day weather forecast with high and low temperatures, weather conditions, and icons.
    - Allows users to add and view weather for multiple locations.
    - Graphical user interface designed using PyQt6.

## Requirements

    - Python 3.6+
    - See `requirements.txt` for the full list of dependencies.

## Setup

    1. **Clone the repository:**
    2. Create a virtual environment and activate it.
    3. Install the required packages: pip install -r requirements.txt
    4. Create a config.py file in the root directory and add your OpenWeatherMap API key: API_KEY = "your_openweathermap_api_key"

## Project Structure

    src/
    |-- main.py: The main entry point of the application.
    |-- Weather.py: Contains the Weather class to fetch and parse current weather data.
    |-- Forecast.py: Contains the Forecast class to fetch and parse 5-day weather forecast data.
    |-- Day.py: Contains the Day class representing a single day's weather data.
    |-- image_loader.py: Contains the ImageLoader class for loading weather icons.
    |-- resources/
    |   |-- icons/: Contains the icon files for the application.
    |   |-- ui/: Contains the .ui files for the application's UI design.
    |-- tests/
    |   |-- test_weather.py: Unit tests for the Weather class.
    |   |-- test_forecast.py: Unit tests for the Forecast class.
    |   |-- test_day.py: Unit tests for the Day class.
    |-- config.py: Configuration file for storing the OpenWeatherMap API key (not included in the repository).

## Usage

    - Add a location:
        Enter the city name in the "Add Location" screen.
        Click the "Enter" button to fetch and display the weather data.

    - View the forecast:
        Click on the "Forecast" button to view the 5-day weather forecast.

    - Clear the weather data:
        Click on the "Clear" button to remove the weather data for the specified location.

## License

    - This project is licensed under the MIT License.

## Acknowledgments

    - OpenWeatherMap for providing the weather data API.
