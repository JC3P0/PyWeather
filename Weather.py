import requests
from datetime import datetime


def convert_to_fahrenheit(kelvin):
    kelvin = kelvin - 273.15
    kelvin = kelvin * 1.8
    kelvin = kelvin + 32
    return round(kelvin)


def convert_to_celsius(kelvin):
    kelvin = kelvin - 273.15
    return format(kelvin, ".2f")


def convert_time(time, timezone):
    time = time + timezone
    datetime_obj = datetime.utcfromtimestamp(time)
    return datetime_obj.strftime("%b %d %I:%M %p")


def convert_sunrise_sunset(time, timezone):
    time = time + timezone
    datetime_obj = datetime.utcfromtimestamp(time)
    return datetime_obj.strftime("%I:%M %p")


class Weather:
    def __init__(self, location):
        self.__location = location
        self.__response = requests.request("GET",
                                           "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&APPID=" + "8f0baa3c0e3577c3c9c5140b55e4343a")
        self.__parse_Json = self.__response.json()
        self.__country = self.__parse_Json["sys"]["country"]
        self.__timezone = self.__parse_Json["timezone"]
        self.__current_weather = self.__parse_Json["weather"][0]["description"]
        self.__current_temp = convert_to_fahrenheit(self.__parse_Json["main"]["temp"])
        self.__humidity = self.__parse_Json["main"]["humidity"]
        self.__wind = self.__parse_Json["wind"]["speed"]
        self.__sunrise = convert_sunrise_sunset(self.__parse_Json["sys"]["sunrise"], self.__timezone)
        self.__sunset = convert_sunrise_sunset(self.__parse_Json["sys"]["sunset"], self.__timezone)
        self.__lon = self.__parse_Json["coord"]["lon"]
        self.__lat = self.__parse_Json["coord"]["lat"]
        self.__time = convert_time(self.__parse_Json["dt"], self.__timezone)

    def get_location(self):
        return self.__location

    def get_lon(self):
        return self.__lon

    def get_lat(self):
        return self.__lat

    def get_timezone(self):
        return self.__timezone

    def __str__(self):
        return f'{self.__location} {self.__country} {self.__current_weather} {self.__current_temp} {self.__humidity} {self.__wind} {self.__sunrise} {self.__sunset} {self.__time}'
