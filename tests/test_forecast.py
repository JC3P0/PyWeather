import unittest
from unittest.mock import patch, Mock

from Forecast import Forecast

class TestForecast(unittest.TestCase):

    @patch('Forecast.requests.get')
    @patch.dict('sys.modules', {'config': Mock(API_KEY='fake_api_key')})
    def test_generate_forecast(self, mock_get):
        # Define the mock response data
        mock_response_data = {
            "list": [
                {
                    "dt": 1600418400,
                    "main": {
                        "temp_max": 292.15,
                        "temp_min": 287.15
                    },
                    "weather": [{"main": "Clear", "icon": "01d"}]
                }
            ]
        }

        # Set up the mock to return the mock response data
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response_data

        # Create a Forecast object and generate forecast data
        forecast = Forecast()
        forecast.generate_forecast(-74.006, 40.7128, -18000)

        # Assert that the forecast object is correctly populated
        self.assertEqual(forecast.forecast_timezone, -18000)
        self.assertEqual(forecast.forecast_lat, -74.006)

    @patch('Forecast.requests.get')
    @patch.dict('sys.modules', {'config': Mock(API_KEY='fake_api_key')})
    def test_forecast_with_invalid_data(self, mock_get):
        # Set up the mock to return an invalid response
        mock_get.return_value = Mock(status_code=404)

        # Create a Forecast object and generate forecast data with invalid input
        forecast = Forecast()
        forecast.generate_forecast(40.7128, "tree", -16000)

        # Assert that the forecast object is not valid
        self.assertIsNone(forecast.average_high)
        self.assertIsNone(forecast.average_low)
        self.assertIsNone(forecast.forecast_lon)
        self.assertIsNone(forecast.forecast_lat)
        self.assertEqual(len(forecast.list), 0)
        self.assertFalse(forecast.is_valid())

if __name__ == '__main__':
    unittest.main()
