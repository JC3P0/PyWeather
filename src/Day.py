import logging
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

@dataclass
class Day:
    day_high: float = None
    day_low: float = None
    day_date: str = None
    day_weather: str = None
    day_weatherIcon: str = None

    def __init__(self, info_list: List[Dict], info_offset: int, timezone_offset: int):
        """
        Initialize a Day object with weather information.
        Parameters:
        - info_list: List of weather information dictionaries.
        - info_offset: Offset to locate the day's weather information.
        - timezone_offset: Timezone offset in seconds.
        """
        self._parse_day_info(info_list, info_offset, timezone_offset)

    def _parse_day_info(self, info_list: List[Dict], info_offset: int, timezone_offset: int):
        """
        Parse and set the day's weather information.
        Parameters:
        - info_list: List of weather information dictionaries.
        - info_offset: Offset to locate the day's weather information.
        - timezone_offset: Timezone offset in seconds.
        """
        try:
            highest = max(info_list[info_offset + i]["main"]["temp_max"] for i in range(8))
            lowest = min(info_list[info_offset + i]["main"]["temp_min"] for i in range(8))

            self.day_high = convert_to_fahrenheit(highest)
            self.day_low = convert_to_fahrenheit(lowest)
            self.day_date = convert_date(info_list[info_offset]["dt"], timezone_offset)
            self.day_weather = info_list[info_offset]["weather"][0]["main"]
            self.day_weatherIcon = info_list[info_offset]["weather"][0]["icon"]
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing day info: {e}")
            raise ValueError(f"Invalid data provided: {e}")

def convert_to_fahrenheit(kelvin):
    """Convert temperature from Kelvin to Fahrenheit."""
    return round((kelvin - 273.15) * 1.8 + 32)

def convert_to_celsius(kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return format(kelvin - 273.15, ".2f")

def convert_date(timestamp, timezone_offset):
    """Convert Unix timestamp to a human-readable date."""
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(seconds=timezone_offset)
    return dt.strftime("%b, %d")

def __str__(self):
    return (f"{self.day_high} {self.day_low} {self.day_date} "
            f"{self.day_weather} {self.day_weatherIcon}")
