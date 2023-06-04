from datetime import datetime


def convert_to_fahrenheit(kelvin):
    kelvin = kelvin - 273.15
    kelvin = kelvin * 1.8
    kelvin = kelvin + 32
    return round(kelvin)


def convert_to_celsius(kelvin):
    kelvin = kelvin - 273.15
    return format(kelvin, ".2f")


def convert_date(time, timezone):
    time = time + timezone
    datetime_obj = datetime.utcfromtimestamp(time)
    return datetime_obj.strftime("%b, %d")


class Day:
    def __init__(self, info_list, info_offset, timezone):
        highest = 0
        lowest = 999
        # # calculate each day high and low temps
        for offset in range(info_offset, info_offset + 8):
            temp_high = info_list[offset]["main"]["temp_max"]
            if temp_high > highest:
                highest = temp_high
            temp_low = info_list[offset]["main"]["temp_min"]
            if temp_low < lowest:
                lowest = temp_low
        self.__day_high = convert_to_fahrenheit(highest)
        self.__day_low = convert_to_fahrenheit(lowest)
        self.__day_date = convert_date(info_list[info_offset]["dt"], timezone)
        # self.__day_date = (info_list[info_offset]["dt"], timezone)
        self.__day_weather = info_list[info_offset]["weather"][0]["main"]
        self.__day_timezone = timezone

    def __str__(self):
        return f'{self.__day_high} {self.__day_low} {self.__day_date} {self.__day_weather}'
