import sys
from PySide6.QtCore import Qt, Property, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from PySide6.QtWidgets import QWidget, QSlider, QStyle, QStyleOptionSlider
from editor.common.math import rangeMap

class Slider(QSlider):
	@Property(int)
	def grooveMargin(self):
		return self._grooveMargin
	@grooveMargin.setter
	def grooveMargin(self, value):
		self._grooveMargin = value

	def __init__(self, parent = None):
		super().__init__(parent)
		self.setOrientation(Qt.Horizontal)
		if sys.platform != 'Darwin': self.mousePressEvent = self.newMousePressEvent
		self._grooveMargin = 0

	def newMousePressEvent(self, evt):
		evt.ignore()
		rect = self.rect()
		l, r = rect.left(), rect.right()
		m = self._grooveMargin
		self.setValue(rangeMap(evt.pos().x(), l + m, r - m, self.minimum(), self.maximum()))

		newPos = QPointF(evt.pos().x(), self.rect().center().y())
		newPosGlobal = self.mapToGlobal(newPos)
		newEvt = QMouseEvent(evt.type(), newPos, newPosGlobal, evt.button(), evt.buttons(), evt.modifiers())
		super().mousePressEvent(newEvt)


class RangeSlider(QWidget):
	minRangeChanged = Signal(int)
	maxRangeChanged = Signal(int)

	@Property(int)
	def grooveHeight(self):
		return self._grooveHeight
	@grooveHeight.setter
	def grooveHeight(self, value):
		self._grooveHeight = value
	@Property(int)
	def grooveRoundRadius(self):
		return self._grooveRoundRadius
	@grooveRoundRadius.setter
	def grooveRoundRadius(self, value):
		self._grooveRoundRadius = value

	@Property(int)
	def handleRadius(self):
		return self._handleRadius
	@handleRadius.setter
	def handleRadius(self, value):
		self._handleRadius = value

	@Property(QColor)
	def grooveBackground(self):
		return self._grooveBackground
	@grooveBackground.setter
	def grooveBackground(self, value):
		self._grooveBackground = value

	@Property(QColor)
	def handleBackground(self):
		return self._handleBackground
	@handleBackground.setter
	def handleBackground(self, value):
		self._handleBackground = value
	@Property(QColor)
	def handleHovered(self):
		return self._handleHovered
	@handleHovered.setter
	def handleHovered(self, value):
		self._handleHovered = value

	def __init__(self, parent = None):
		super().__init__(parent)
		self.minimum = 0
		self.maximum = 100
		self.rangeMin = 20
		self.rangeMax = 80
		self.singleStep = 1

		self._grooveHeight = 2
		self._grooveRoundRadius = 0
		self._handleRadius = 6
		self._grooveBackground = QColor('#777')
		self._handleBackground = QColor('#888')
		self._handleHovered = QColor('#ddd')

		self._mouseEntered = False

	def paintEvent(self, evt):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.transparent)

		rect = self.rect()
		w, h = rect.width(), rect.height()

		l, r = self._handleRadius + 1, w - self._handleRadius
		rangeMinX = round(rangeMap(self.rangeMin, self.minimum, self.maximum, l, r))
		rangeMaxX = round(rangeMap(self.rangeMax, self.minimum, self.maximum, l, r))
		centerY = round(h / 2)

		# draw groove
		painter.setBrush(self._grooveBackground)
		grooveTop = centerY - self._grooveHeight / 2
		grooveRectL = QRectF(0, grooveTop, rangeMinX - 1, self._grooveHeight)
		grooveRectR = QRectF(rangeMaxX, grooveTop, w - rangeMaxX, self._grooveHeight)
		grooveRound = round(self._grooveRoundRadius)
		painter.drawRoundedRect(grooveRectL, grooveRound, grooveRound)
		painter.drawRoundedRect(grooveRectR, grooveRound, grooveRound)

		# draw handles
		brush = self._handleHovered if self._mouseEntered else self._handleBackground
		painter.setBrush(brush)

		handleY = centerY - self._handleRadius
		handleSize = self._handleRadius * 2
		startAngle, spanAngle = 90 * 16, 180 * 16
		painter.drawPie(rangeMinX - self._handleRadius - 1, handleY, handleSize, handleSize, startAngle, spanAngle)
		painter.drawPie(rangeMaxX - self._handleRadius, handleY, handleSize, handleSize, -startAngle, spanAngle)

		# draw range rect
		painter.setBrush(self._handleBackground)
		rw = rangeMaxX - rangeMinX - 1
		if rw > 0: painter.drawRect(rangeMinX, centerY - self._handleRadius, rw, self._handleRadius * 2)


	def enterEvent(self, evt):
		self._mouseEntered = True
		self.repaint()
	def leaveEvent(self, evt):
		self._mouseEntered = False
		self.repaint()

	def mousePressEvent(self, evt):
		x = evt.localPos().x()
		l, r = self._handleRadius + 1, self.rect().width() - self._handleRadius
		value = round(rangeMap(x, l, r, self.minimum, self.maximum))
		if value >= self.rangeMax: self._moveTarget = 1
		elif value <= self.rangeMin: self._moveTarget = -1
		else: self._moveTarget = self.rangeMax - value < value - self.rangeMin and 1 or -1
		self.mouseMoveEvent(evt)

	def mouseMoveEvent(self, evt):
		x = evt.localPos().x()
		radius = self._handleRadius
		l, r = radius + 1, self.rect().width() - radius
		if self._moveTarget == 1:
			value = max(round(rangeMap(x - radius, l, r, self.minimum, self.maximum)), self.rangeMin)
			if self.rangeMax != value:
				self.maxRangeChanged.emit(value)
				self.rangeMax = value
				self.repaint()
		else:
			value = min(round(rangeMap(x + radius, l, r, self.minimum, self.maximum)), self.rangeMax)
			if self.rangeMin != value:
				self.minRangeChanged.emit(value)
				self.rangeMin = value
				self.repaint()
