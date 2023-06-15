import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Forecast import Forecast
from Weather import Weather


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainWindow.ui", self)
        # self.UiComponents()
        # self.button_forecast0 = QPushButton("Forecast", self)
        # # widget.addWidget(self.button_forecast0)
        # self.button_forecast1 = QPushButton("Forecast", self)
        # self.button_forecast2 = QPushButton("Forecast", self)
        # self.button_add0 = QPushButton("+", self)
        # self.button_add1 = QPushButton("+", self)
        # self.button_add2 = QPushButton("+", self)
        self.button_forecast0.clicked.connect(self.gotoScreenForecast)
        # self.button_forecast0.hide()
        self.button_forecast1.clicked.connect(self.gotoScreenForecast)
        self.button_forecast2.clicked.connect(self.gotoScreenForecast)
        self.button_add0.clicked.connect(self.gotoScreenAddLocation)
        self.button_add1.clicked.connect(self.gotoScreenAddLocation)
        self.button_add2.clicked.connect(self.gotoScreenAddLocation)

    def gotoScreenForecast(self):
        # screenForecast = ScreenForecast()
        # widget.addWidget(screenForecast)
        widget.setFixedWidth(600)
        widget.setFixedHeight(350)
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def gotoScreenAddLocation(self):
        # screenAddLocation = ScreenAddLocation()
        # widget.addWidget(screenAddLocation)
        widget.setFixedWidth(425)
        widget.setFixedHeight(275)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ScreenAddLocation(QDialog):
    def __init__(self):
        super(ScreenAddLocation, self).__init__()

        loadUi("ScreenAddLocation.ui", self)
        self.buttonBack.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        # main_window = MainWindow()
        # widget.addWidget(main_window)
        widget.setFixedWidth(900)
        widget.setFixedHeight(600)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class ScreenForecast(QDialog):
    def __init__(self):
        super(ScreenForecast, self).__init__()
        loadUi("ScreenForecast.ui", self)
        self.buttonBack.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        # main_window = MainWindow()
        # widget.addWidget(main_window)
        widget.setFixedWidth(900)
        widget.setFixedHeight(600)
        widget.setCurrentIndex(widget.currentIndex() - 2)


# app = QtWidgets.QApplication(sys.argv)
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
main_window = MainWindow()
widget.addWidget(main_window)
add_location = ScreenAddLocation()
widget.addWidget(add_location)
forecast = ScreenForecast()
widget.addWidget(forecast)
widget.setFixedWidth(900)
widget.setFixedHeight(600)
widget.show()

# PyQt6
app.exec()

# PyQt5
# try:
#     sys.exit(app.exec_())
# except:
#     print("Exiting")


def main():
    my_weather = Weather("Carlsbad")
    my_forecast = Forecast(my_weather.get_location(), my_weather.get_lon(), my_weather.get_lat(),
                           my_weather.get_timezone())
    print(my_weather)
    print(my_forecast)
    # parse = my_forecast.get_parse_Json()
    # print(parse)


if __name__ == '__main__':
    main()
