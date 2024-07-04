import requests
import logging
from dataclasses import dataclass, field
from typing import List, Dict
from ConfigManager import ConfigManager
from Day import Day

logging.basicConfig(level=logging.INFO)

@dataclass
class Forecast:
    lat: float = None
    lon: float = None
    timeZone: int = None
    days: List[Day] = field(default_factory=list)
    average_high: float = None
    average_low: float = None

    @staticmethod
    def fetch_forecast_for_location(lat, lon):
        """
        Fetch forecast data for the specified location.
        """
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            logging.error("Invalid latitude or longitude values.")
            return Forecast()  # Return an empty Forecast object

        config = ConfigManager.load_config()
        api_key = config.get('Settings', 'api_key', fallback=None)

        if not api_key:
            logging.error("API key is missing or empty in config")
            return Forecast()  # Return an empty Forecast object

        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch forecast data: {e}")
            return Forecast()  # Return an empty Forecast object

        if response.status_code == 200:
            data = response.json()
            return Forecast._parse_forecast_data(data, lat, lon)

    @staticmethod
    def _parse_forecast_data(data, lat, lon):
        """
        Parse the JSON data to create a Forecast object.
        """
        weather_array = data.get('list', [])
        days = []
        time_zone = data.get('city', {}).get('timezone', 0)

        for i in range(0, len(weather_array), 8):  # Every 8 entries represent a new day (3-hour intervals, 24 hours/day)
            days.append(Day(weather_array, i, time_zone))

        forecast = Forecast(lat, lon, time_zone, days)
        forecast._calculate_averages()
        return forecast

    def _calculate_averages(self):
        """
        Calculate the average high and low temperatures.
        """
        if not self.days:
            self.average_high = 0
            self.average_low = 0
            return

        highs = [day.day_high for day in self.days]
        lows = [day.day_low for day in self.days]

        self.average_high = sum(highs) / len(highs)
        self.average_low = sum(lows) / len(lows)

    def is_empty(self):
        """
        Check if the forecast object is empty.
        """
        return not self.days

    def __str__(self):
        return '\n'.join(str(day) for day in self.days)
