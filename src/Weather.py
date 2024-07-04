import requests
import logging
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from ConfigManager import ConfigManager

logging.basicConfig(level=logging.INFO)

@dataclass
class Weather:
    name: str = None
    current_temp: float = None
    max_temp: float = None
    min_temp: float = None
    humidity: int = None
    visibility: float = None
    timezone: int = None
    sunrise: str = None
    sunset: str = None
    lon: float = None
    lat: float = None
    description: str = None
    country: str = None
    wind: float = None
    icon: str = None
    time: str = None
    
    def generate_weather(self, city):
        """
        Generate weather data for the specified city.
        """
        config = ConfigManager.load_config()
        api_key = config.get('Settings', 'api_key', fallback=None)

        if not api_key:
            logging.error("API key is missing or empty in config")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.replace(' ', '+')}&APPID={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch weather data.")
            return

        if response.status_code == 200:
            self._parse_weather_data(data)

    def _parse_weather_data(self, data):
        """
        Parse the weather data from the API response.
        """
        try:
            main = data.get("main", {})
            sys = data.get("sys", {})
            coord = data.get("coord", {})
            weather = data.get("weather", [{}])[0]
            wind = data.get("wind", {})
            
            self.name = data.get("name")
            self.wind = wind.get("speed")
            self.description = weather.get("description")
            self.icon = weather.get("icon")
            self.current_temp = self.kelvin_to_fahrenheit(main.get("temp"))
            self.max_temp = self.kelvin_to_fahrenheit(main.get("temp_max"))
            self.min_temp = self.kelvin_to_fahrenheit(main.get("temp_min"))
            self.humidity = main.get("humidity")
            self.visibility = data.get("visibility", 0) / 1000
            self.sunrise = self.convert_time(sys.get("sunrise"), data.get("timezone"))
            self.sunset = self.convert_time(sys.get("sunset"), data.get("timezone"))
            self.country = sys.get("country")
            self.timezone = data.get("timezone")
            self.lon = coord.get("lon")
            self.lat = coord.get("lat")
            self.time = self.convert_date(data.get("dt"), data.get("timezone"))
        except KeyError as e:
            logging.error(f"Key error: {e}")
        except Exception as e:
            logging.error(f"Error parsing weather data: {e}")

    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        if kelvin is None:
            return None
        return round((kelvin - 273.15) * 9 / 5 + 32)

    @staticmethod
    def convert_date(timestamp, timezone_offset):
        if timestamp is None or timezone_offset is None:
            return None
        local_time = datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(seconds=timezone_offset)
        return local_time.strftime("%B %d,\n%I:%M %p")

    @staticmethod
    def convert_time(timestamp, timezone_offset):
        if timestamp is None or timezone_offset is None:
            return None
        local_time = datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(seconds=timezone_offset)
        return local_time.strftime("%I:%M %p")
    
    def is_valid(self):
        """
        Check if the weather object has been properly initialized with valid data.
        """
        required_fields = [
            self.current_temp, self.max_temp, self.min_temp,
            self.humidity, self.visibility, self.timezone,
            self.sunrise, self.sunset, self.lon, self.lat,
            self.description, self.country, self.name,
            self.wind, self.icon, self.time
        ]
        return all(field is not None for field in required_fields)

    def __str__(self):
        return (f"City: {self.name}\n"
                f"Current Temp: {self.current_temp}\n"
                f"Max Temp: {self.max_temp}\n"
                f"Min Temp: {self.min_temp}\n"
                f"Description: {self.description}\n"
                f"Humidity: {self.humidity}\n"
                f"Visibility: {self.visibility}\n"
                f"Wind: {self.wind}\n"
                f"Sunrise: {self.sunrise}\n"
                f"Sunset: {self.sunset}\n"
                f"Country: {self.country}\n"
                f"Timezone: {self.timezone}\n"
                f"Longitude: {self.lon}\n"
                f"Latitude: {self.lat}\n"
                f"Data Time: {self.time}\n")
