import unittest
from Day import Day
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class TestDay(unittest.TestCase):

    def setUp(self):
        # Correct data
        self.correct_info_list = [
            {"main": {"temp_max": 310, "temp_min": 300}, "dt": 1622520000, "weather": [{"main": "Clear", "icon": "01d"}]},
            {"main": {"temp_max": 311, "temp_min": 299}, "dt": 1622606400, "weather": [{"main": "Clouds", "icon": "02d"}]},
            {"main": {"temp_max": 312, "temp_min": 298}, "dt": 1622692800, "weather": [{"main": "Rain", "icon": "09d"}]},
            {"main": {"temp_max": 313, "temp_min": 297}, "dt": 1622779200, "weather": [{"main": "Thunderstorm", "icon": "11d"}]},
            {"main": {"temp_max": 314, "temp_min": 296}, "dt": 1622865600, "weather": [{"main": "Snow", "icon": "13d"}]},
            {"main": {"temp_max": 315, "temp_min": 295}, "dt": 1622952000, "weather": [{"main": "Mist", "icon": "50d"}]},
            {"main": {"temp_max": 316, "temp_min": 294}, "dt": 1623038400, "weather": [{"main": "Haze", "icon": "04d"}]},
            {"main": {"temp_max": 317, "temp_min": 293}, "dt": 1623124800, "weather": [{"main": "Fog", "icon": "04d"}]}
        ]
        
        # Incorrect data that will cause KeyError
        self.incorrect_info_list = [
            {"main": {"temp_max": 310}, "dt": 1622520000, "weather": [{"main": "Clear", "icon": "01d"}]},
            {"main": {"temp_max": 311, "temp_min": 299}, "dt": 1622606400, "weather": [{"main": "Clouds"}]},  # Missing icon
            {"main": {"temp_max": 312, "temp_min": 298}, "dt": 1622692800},  # Missing weather
            {"main": {"temp_min": 297}, "dt": 1622779200, "weather": [{"main": "Thunderstorm", "icon": "11d"}]},  # Missing temp_max
        ]

    def test_day_with_correct_data(self):
        day = Day(self.correct_info_list, 0, 0)
        self.assertEqual(day.day_high, 111)
        self.assertEqual(day.day_low, 68)
        self.assertEqual(day.day_date, "Jun, 01")
        self.assertEqual(day.day_weather, "Clear")
        self.assertEqual(day.day_weatherIcon, "01d")

    def test_day_with_incorrect_data(self):
        # This test should trigger the logging error
        with self.assertRaises(ValueError):
            day = Day(self.incorrect_info_list, 0, 0)

if __name__ == '__main__':
    unittest.main()
