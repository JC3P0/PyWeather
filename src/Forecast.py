import requests
import statistics
import logging
from dataclasses import dataclass, field
from typing import List, Dict
from Day import Day

logging.basicConfig(level=logging.INFO)

@dataclass
class Forecast:
    forecast_lon: float = None
    forecast_lat: float = None
    forecast_timezone: int = None
    list: List[Day] = field(default_factory=list)
    average_high: float = None
    average_low: float = None
    parse_json: Dict = field(default_factory=dict)

    def generate_forecast(self, lat, lon, timezone):
        """
        Fetch forecast data from the API.
        """
        try:
            from config import API_KEY
        except ImportError:
            raise ImportError("No API key found. Create a config.py file with your API key.")
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error("Failed to fetch forecast data.")
            return
        
        if response.status_code == 200:
            self.forecast_timezone = timezone
            self.forecast_lon = lon
            self.forecast_lat = lat
            data = response.json()
            self.parse_json = data
            self._set_forecast_data(data)

    def _set_forecast_data(self, data):
        # Create forecast days
        self.list = self._create_forecast_days()
        # Calculate average high and low temperatures
        self.average_high = self._calculate_average_high()
        self.average_low = self._calculate_average_low()

    def _create_forecast_days(self):
        """
        Create Day objects for the forecast.
        """
        if "list" not in self.parse_json:
            return []

        list_offsets = [0, 8, 16, 24, 32]
        return [Day(self.parse_json["list"], offset, self.forecast_timezone) for offset in list_offsets if len(self.parse_json["list"]) > offset + 7]

    def _calculate_average_high(self):
        """
        Calculate the average high temperature.
        """
        if not self.list:
            return 0
        highs = [float(day.day_high) for day in self.list]
        return round(statistics.mean(highs))

    def _calculate_average_low(self):
        """
        Calculate the average low temperature.
        """
        if not self.list:
            return 0
        lows = [float(day.day_low) for day in self.list]
        return round(statistics.mean(lows))
    
    def is_valid(self):
        """
        Check if the forecast object has been properly initialized with valid data.
        """
        required_fields = [
            self.forecast_lon, self.forecast_lat, self.forecast_timezone, self.list, self.parse_json
        ]
        return all(field is not None and field != {} for field in required_fields) and len(self.list) > 0

    def __str__(self):
        return f'{self.list[0]} {self.list[1]} {self.list[2]} {self.list[3]} {self.list[4]}'
