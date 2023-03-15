from PySide6.QtCore import Qt, Property, QRectF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from editor.common.math import locAt

class ProgressBar(QWidget):
	@Property(int)
	def progressHeight(self):
		return self._height
	@progressHeight.setter
	def progressHeight(self, value):
		self._height = value
	@Property(int)
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value

	@Property(QColor)
	def borderColor(self):
		return self._borderColor
	@borderColor.setter
	def borderColor(self, value):
		self._borderColor = value

	@Property(QColor)
	def background(self):
		return self._background
	@background.setter
	def background(self, value):
		self._background = value

	@Property(QColor)
	def overlay(self):
		return self._overlay
	@overlay.setter
	def overlay(self, value):
		self._overlay = value

	def __init__(self, parent = None):
		super().__init__(parent)
		self.minimum = 0
		self.maximum = 100
		self.value = 20

		self._height = 6
		self._borderRadius = 3
		self._borderColor = Qt.transparent
		self._background = QColor('#282828')
		self._overlay = QColor('#0071ff')

	def setValue(self, value):
		self.value = value
		self.repaint()

	def paintEvent(self, evt):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(self._borderColor)

		rect = self.rect()
		w, h = rect.width(), rect.height()
		x = rect.x()
		cy = round(h / 2)
		t = cy - self._height / 2
		r = round(self._borderRadius)

		# draw background
		painter.setBrush(self._background)
		brect = QRectF(x, t, w, self._height)
		painter.drawRoundedRect(brect, r, r)

		# draw overlay
		painter.setPen(Qt.transparent)
		painter.setBrush(self._overlay)
		k = locAt(self.minimum, self.maximum, self.value)
		orect = QRectF(x, t, w * k, self._height)
		painter.drawRoundedRect(orect, r, r)
