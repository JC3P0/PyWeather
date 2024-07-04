import requests
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

class ImageLoader(QThread):
    image_loaded = pyqtSignal(int, QPixmap, object)

    def __init__(self, index, icon_url, target):
        super().__init__()
        self.index = index
        self.icon_url = icon_url
        self.target = target

    def run(self):
        try:
            response = requests.get(self.icon_url)
            response.raise_for_status()
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_loaded.emit(self.index, pixmap, self.target)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch image for URL {self.icon_url}")
