import unittest
from unittest.mock import patch, Mock

from Weather import Weather

class TestWeather(unittest.TestCase):

    @patch('Weather.requests.get')
    @patch.dict('sys.modules', {'config': Mock(API_KEY='fake_api_key')})
    def test_generate_weather(self, mock_get):
        # Define the mock response data
        mock_response_data = {
            "name": "London",
            "main": {
                "temp": 289.92,
                "temp_max": 292.15,
                "temp_min": 287.15,
                "humidity": 82
            },
            "visibility": 10000,
            "wind": {"speed": 4.1},
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "sys": {"country": "GB", "sunrise": 1600394511, "sunset": 1600438501},
            "timezone": 3600,
            "coord": {"lon": -0.1257, "lat": 51.5085},
            "dt": 1600418400
        }

        # Set up the mock to return the mock response data
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response_data

        # Create a Weather object and generate weather data
        weather = Weather()
        weather.generate_weather("London")

        # Debugging output to check field values
        for field_name, field_value in vars(weather).items():
            print(f"{field_name}: {field_value}")

        # Assert that the weather object is correctly populated
        self.assertTrue(weather.is_valid())
        self.assertEqual(weather.name, "London")
        self.assertEqual(weather.current_temp, Weather.kelvin_to_fahrenheit(289.92))
        self.assertEqual(weather.max_temp, Weather.kelvin_to_fahrenheit(292.15))
        self.assertEqual(weather.min_temp, Weather.kelvin_to_fahrenheit(287.15))
        self.assertEqual(weather.humidity, 82)
        self.assertEqual(weather.description, "clear sky")
        self.assertEqual(weather.icon, "01d")
        self.assertEqual(weather.country, "GB")
        self.assertEqual(weather.timezone, 3600)
        self.assertEqual(weather.lon, -0.1257)
        self.assertEqual(weather.lat, 51.5085)

    def test_kelvin_to_fahrenheit(self):
        # Test the static method for converting Kelvin to Fahrenheit
        self.assertEqual(Weather.kelvin_to_fahrenheit(273.15), 32)
        self.assertEqual(Weather.kelvin_to_fahrenheit(300), 80)

    def test_convert_date(self):
        # Test the static method for converting Unix timestamp to date
        self.assertEqual(Weather.convert_date(1600418400, 3600), "September 18,\n09:40 AM")

if __name__ == '__main__':
    unittest.main()
