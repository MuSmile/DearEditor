from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget
from editor.tools.icon_cache import getThemePixmap

class PixmapIcon(QWidget):
    def __init__(self, width, height, pixmap = None, parent = None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.pixmap = pixmap and getThemePixmap(pixmap)

    def setPixmap(self, pixmap):
        self.pixmap = getThemePixmap(pixmap)
        self.update()

    def paintEvent(self, evt):
        if not self.pixmap: return
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing, True)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawPixmap(self.rect(), self.pixmap)
