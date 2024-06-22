import sys
import os
import re
import logging
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QMessageBox, QGraphicsScene
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPixmap, QIcon

# Add src directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Forecast import Forecast
from Weather import Weather
from image_loader import ImageLoader  # Import the ImageLoader class

logging.basicConfig(level=logging.INFO)

def resource_path(resource_type, relative_path):
    """Get absolute path to resource, works for development and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Adjust the base_path to go up one level from 'src'
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

    return os.path.join(base_path, resource_type, relative_path)

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(resource_path('ui', 'MainWindow.ui'), self)
        self.weather_objects = [Weather() for _ in range(3)]
        self.clear_fields()
        self.setup_graphics_views()
        self.setup_buttons()
        self.module = 0
        self.setup_timer()
        self.populate_fields()
        self.image_loaders = []  # List to keep references to ImageLoader threads

    def setup_buttons(self):
        """Connect buttons to their respective methods."""
        for i in range(3):
            getattr(self, f'button_clear{i}').clicked.connect(self.clear_button_clicked)
            getattr(self, f'button_forecast{i}').clicked.connect(self.forecast_button_clicked)
            getattr(self, f'button_add{i}').clicked.connect(self.add_button_clicked)

    def setup_graphics_views(self):
        """Setup graphics views."""
        for i in range(3):
            self.setup_graphics_view(getattr(self, f'graphicsView_main{i}'))

    def setup_graphics_view(self, graphics_view):
        """Setup a single graphics view."""
        graphics_view.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        graphics_view.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Ensure image is centered

    def setup_timer(self):
        """Setup the timer for periodic updates."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.populate_fields)
        self.timer.start(600000)  # 600000 milliseconds = 10 min

    def add_button_clicked(self):
        """Handle add button click."""
        button = self.sender()
        self.module = int(button.objectName()[-1])
        switch_window(widget, widget.currentIndex() + 1, 425, 275)

    def clear_button_clicked(self):
        """Handle clear button click."""
        button = self.sender()
        index = int(button.objectName()[-1])
        self.weather_objects[index] = Weather()
        self.clear_fields()

    def forecast_button_clicked(self):
        """Handle forecast button click."""
        button = self.sender()
        index = int(button.objectName()[-1])
        forecast.set_forecast(self.weather_objects[index].name, self.weather_objects[index].lat, self.weather_objects[index].lon, self.weather_objects[index].country, self.weather_objects[index].timezone)
        switch_window(widget, widget.currentIndex() + 2, 600, 350)

    def set_graphics_view_image(self, index, icon_code):
        """Set image for a graphics view."""
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        loader = ImageLoader(index, icon_url, self)  # Pass the main window as target
        loader.image_loaded.connect(self.update_graphics_view)
        self.image_loaders.append(loader)  # Keep a reference to the loader
        loader.start()

    def update_graphics_view(self, index, pixmap, target):
        if isinstance(target, MainWindow):
            scene = QGraphicsScene()
            scene.addPixmap(pixmap)
            scene.setSceneRect(QRectF(pixmap.rect()))  # Ensure the scene rect matches the pixmap
            graphics_view = getattr(target, f'graphicsView_main{index}')
            graphics_view.setScene(scene)
            graphics_view.fitInView(scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Fit the scene within the view
        elif isinstance(target, ScreenForecast):
            scene = QGraphicsScene()
            scene.addPixmap(pixmap)
            scene.setSceneRect(QRectF(pixmap.rect()))  # Ensure the scene rect matches the pixmap
            graphics_view = getattr(target, f'graphicsView_forecast{index}')
            graphics_view.setScene(scene)
            graphics_view.fitInView(scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Fit the scene within the view

    def set_weather_obj(self, city):
        """Set weather object based on the module index."""
        self.weather_objects[self.module].generate_weather(city)

    def populate_fields(self):
        """Populate fields with weather data."""
        for i in range(3):
            if self.weather_objects[i].is_valid():
                self.set_field(i)

    def set_field(self, index):
        """Set fields for a specific weather object."""
        weather_obj = self.weather_objects[index]
        city = weather_obj.name
        weather_obj.generate_weather(city)
        getattr(self, f'day{index}Temp').setText(f"{weather_obj.current_temp}°F")
        getattr(self, f'day{index}Loc').setText(f"{weather_obj.name}, {weather_obj.country}")
        getattr(self, f'day{index}Desc').setText(weather_obj.description)
        getattr(self, f'day{index}SunRise').setText(weather_obj.sunrise)
        getattr(self, f'day{index}SunSet').setText(weather_obj.sunset)
        getattr(self, f'day{index}Date').setText(weather_obj.time)
        getattr(self, f'day{index}Humid').setText(f"\U0001F4A7 \n{weather_obj.humidity}% Humidity")
        getattr(self, f'day{index}Wind').setText(f"\U0001F4A8 \nWind {round(weather_obj.wind)} mph")
        getattr(self, f'day{index}RiseLabel').show()
        getattr(self, f'day{index}SetLabel').show()
        getattr(self, f'day{index}RiseSymb').show()
        getattr(self, f'day{index}SetSymb').show()
        getattr(self, f'graphicsView_main{index}').show()
        getattr(self, f'button_forecast{index}').show()
        getattr(self, f'button_add{index}').hide()
        getattr(self, f'addLocation{index}').hide()
        getattr(self, f'button_clear{index}').show()
        self.set_graphics_view_image(index, weather_obj.icon)

    def clear_fields(self):
        """Clear fields for invalid weather objects."""
        for i in range(3):
            if not self.weather_objects[i].is_valid():
                self.clear_fields_with_index(i)

    def clear_fields_with_index(self, index):
        """Clear fields for a specific weather object."""
        for attr in ['Temp', 'Loc', 'Desc', 'Humid', 'Wind', 'SunRise', 'SunSet', 'Date']:
            getattr(self, f'day{index}{attr}').setText("")
        for attr in ['RiseLabel', 'SetLabel', 'RiseSymb', 'SetSymb']:
            getattr(self, f'day{index}{attr}').hide()
        getattr(self, f'button_clear{index}').hide()
        getattr(self, f'graphicsView_main{index}').hide()
        getattr(self, f'button_forecast{index}').hide()
        getattr(self, f'button_add{index}').show()
        getattr(self, f'addLocation{index}').show()

class ScreenForecast(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(resource_path('ui', 'ScreenForecast.ui'), self)
        self.buttonBack.clicked.connect(self.goto_main_window)
        self.setup_graphics_forecast_views()
        self.image_loaders = []  # List to keep references to ImageLoader threads

    def setup_graphics_forecast_views(self):
        """Setup graphics views for forecast images."""
        for i in range(5):
            self.setup_graphics_forecast_view(getattr(self, f'graphicsView_forecast{i}'))

    def setup_graphics_forecast_view(self, graphics_view):
        """Setup a single graphics view for forecast."""
        graphics_view.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        graphics_view.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Ensure image is centered

    def set_graphics_view_forecast_image(self, index, icon_code):
        """Set image for a forecast graphics view."""
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        loader = ImageLoader(index, icon_url, self)  # Pass the forecast screen as target
        loader.image_loaded.connect(main_window.update_graphics_view)
        self.image_loaders.append(loader)  # Keep a reference to the loader
        loader.start()

    def set_forecast(self, city_name, city_lat, city_lon, city_country, city_timezone):
        """Set the forecast for the next 5 days."""
        forecast = Forecast()
        forecast.generate_forecast(city_lat, city_lon, city_timezone)
        self.forecastCity.setText(f"{city_name}, {city_country}")

        for i in range(5):
            self.set_day_forecast(forecast, i)

        self.fiveDayHighAvg.setText(str(forecast.average_high))
        self.fiveDayLowAvg.setText(str(forecast.average_low))

    def set_day_forecast(self, forecast, index):
        """Set the forecast for a specific day."""
        day = forecast.list[index]
        getattr(self, f'day{index}High').setText(str(day.day_high))
        getattr(self, f'day{index}Low').setText(str(day.day_low))
        getattr(self, f'day{index}Date').setText(str(day.day_date))
        getattr(self, f'day{index}Desc').setText(str(day.day_weather))
        self.set_graphics_view_forecast_image(index, str(day.day_weatherIcon))

    def goto_main_window(self):
        """Return to the main window."""
        main_window.populate_fields()
        switch_window(widget, widget.currentIndex() - 2, 900, 600)

class ScreenAddLocation(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(resource_path('ui', 'ScreenAddLocation.ui'), self)
        self.buttonBack.clicked.connect(self.goto_main_window)
        
    def goto_main_window(self):
        city = self.lineEditCity.text().strip().replace(" ", "+")
        current_weather = Weather()
        current_weather.generate_weather(city)
        self.lineEditCity.setText("")

        if current_weather.is_valid() and re.match(r'^[a-zA-Z\s-]+$', city.replace("+", " ")) and 1 <= len(city.replace("+", " ")) <= 50:
            main_window.set_weather_obj(city)
            main_window.populate_fields()
            switch_window(widget, widget.currentIndex() - 1, 900, 600)
        else:
            QMessageBox.critical(self, "Invalid City", "The city entered is not valid. Please try again.")

def switch_window(widget, index, width, height):
    widget.setFixedWidth(width)
    widget.setFixedHeight(height)
    widget.setCurrentIndex(index)
    center_window(widget)

def center_window(widget):
    """Center the window on the screen."""
    qr = widget.frameGeometry()
    cp = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())

def main():
    try:
        app_icon_path = resource_path('icons', 'app_icon.png')
    except ImportError:
        raise ImportError("No icon path found.")
    
    app = QApplication(sys.argv)
    global widget, main_window, forecast
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle("PyWeather")
    widget.setWindowIcon(QIcon(app_icon_path))
    main_window = MainWindow()
    widget.addWidget(main_window)
    widget.addWidget(ScreenAddLocation())
    forecast = ScreenForecast()
    widget.addWidget(forecast)
    widget.setFixedWidth(900)
    widget.setFixedHeight(600)
    center_window(widget)
    widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
