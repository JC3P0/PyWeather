import requests
import statistics
from Day import Day


class Forecast:
    def __init__(self, location, lon, lat, timezone):
        self.__forecast_location = location
        self.__forecast_lon = lon
        self.__forecast_lat = lat
        self.__forecast_timezone = timezone
        self.__response = requests.request("GET",
                                           "https://api.openweathermap.org/data/2.5/forecast?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + "8f0baa3c0e3577c3c9c5140b55e4343a")
        self.__parse_Json = self.__response.json()
        self.__list = []
        self.__list.append((Day(self.__parse_Json["list"], 0, timezone)))
        self.__list.append((Day(self.__parse_Json["list"], 8, timezone)))
        self.__list.append((Day(self.__parse_Json["list"], 16, timezone)))
        self.__list.append((Day(self.__parse_Json["list"], 24, timezone)))
        self.__list.append((Day(self.__parse_Json["list"], 32, timezone)))
        high_avg = statistics.mean((float(obj._Day__day_high) for obj in self.__list))
        low_avg = statistics.mean((float(obj._Day__day_low) for obj in self.__list))
        self.__average_high = round(high_avg)
        self.__average_low = round(low_avg)

    def get_parse_Json(self):
        return self.__parse_Json

    def __str__(self):
        return f'{self.__forecast_location} {self.__list[0]} {self.__list[1]} {self.__list[2]} {self.__list[3]} {self.__list[4]}'
