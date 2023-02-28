import time
from enum import Enum
from PySide6.QtCore import Qt, QRectF, QPoint, Signal, Property
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from editor.tools.util import lerp, rangeMap

class SliderState(Enum):
	Normal  = 0
	Hovered = 1
	Pressed = 2

# default configs
_valueUpdateInterval = 0.05

_brushHandleNormal  = QBrush(QColor(120, 120, 120))
_brushHandleHovered = QBrush(QColor(100, 100, 100))
_brushHandlePressed = QBrush(QColor(100, 100, 100))
_brushHandleOutter  = QBrush(QColor(50, 100, 180, 100))
_brushGrooveNormal  = QBrush(QColor(120, 120, 120))
_brushGrooveHovered = _brushGrooveNormal
_brushGroovePressed = _brushGrooveNormal

class Slider(QWidget):
	valueChanged = Signal(float)

	def __init__(self, minv = 0, maxv = 1, value = None, step = None, parent = None):
		super().__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setFocusPolicy(Qt.StrongFocus)
		# self.setFocusPolicy(Qt.NoFocus)

		self._grooveHeight = 2
		self._grooveRoundRadius = 0

		self._handleRadius = 6
		self._handleOutterRadius = self._handleRadius + 4
		self.setFixedHeight(self._handleOutterRadius * 2)

		self.minValue = minv
		self.maxValue = maxv
		self.value = value or minv
		self.step = step

		self.state = None
		self.focused = False
		self.lastTriggerSignalTime = 0
		self._updateState(SliderState.Normal)

	################ API ################
	def setValue(self, value):
		if self.value == value: return
		self.value = value
		self.update()

	################ Properties ################
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

	@Property(int)
	def handleRadius(self):
		return self._handleRadius
	@handleRadius.setter
	def handleRadius(self, value):
		self._handleRadius = value

	@Property(int)
	def handleOutterRadius(self):
		return self._handleOutterRadius
	@handleOutterRadius.setter
	def handleOutterRadius(self, value):
		self._handleOutterRadius = value

	################ Impl ################
	def paintEvent(self,event):
		painter=QPainter()
		painter.begin(self)
		painter.setRenderHints(QPainter.Antialiasing, True)
		painter.setPen(Qt.transparent)

		rect = self.rect()
		rw, rh = rect.width(), rect.height()
		
		# draw test bg rect
		# painter.setBrush(QBrush(QColor(100, 100, 100, 80)))
		# painter.drawRect(rect)

		left = self._handleOutterRadius
		right = rw - self._handleOutterRadius
		handleX = rangeMap(self.value, self.minValue, self.maxValue, left, right)
		handleY = rh / 2

		# draw groove rect
		painter.setBrush(self.brushGroove)
		left = self._handleOutterRadius / 2
		right = rw - self._handleOutterRadius / 2
		grooveRect = QRectF(left, handleY - self._grooveHeight/2, right-left, self._grooveHeight)
		grooveRound = round(self._grooveRoundRadius)
		painter.drawRoundedRect(grooveRect, grooveRound, grooveRound)

		# draw handle outter circle
		if self.focused or self.state == SliderState.Pressed:
			painter.setBrush(_brushHandleOutter)
			painter.drawEllipse(
				round(handleX - self._handleOutterRadius),
				round(handleY - self._handleOutterRadius),
				self._handleOutterRadius * 2, self._handleOutterRadius * 2)
		
		# draw handle inner circle
		painter.setBrush(self.brushHandle)
		painter.drawEllipse(
			round(handleX - self._handleRadius),
			round(handleY - self._handleRadius),
			self._handleRadius * 2, self._handleRadius * 2)

		painter.end()

	def _updateState(self, state):
		if self.state == state: return

		if state == SliderState.Hovered:
			self.brushHandle = _brushHandleHovered
			self.brushGroove = _brushGrooveHovered
		elif state == SliderState.Pressed:
			self.brushHandle = _brushHandlePressed
			self.brushGroove = _brushGroovePressed
		else:
			self.brushHandle = _brushHandleNormal
			self.brushGroove = _brushGrooveNormal

		self.state = state
		self.update()

	def _updateFocused(self, focused):
		if self.focused == focused: return
		self.focused = focused
		self.update()

	def focusInEvent(self, evt):
		self._updateFocused(True)
	def focusOutEvent(self, evt):
		self._updateFocused(False)
		self._updateState(SliderState.Normal)

	def enterEvent(self, evt):
		if self.focused: return
		if self.state != SliderState.Normal: return
		self._updateState(SliderState.Hovered)
	def leaveEvent(self, evt):
		if self.focused: return
		if self.state != SliderState.Hovered: return
		self._updateState(SliderState.Normal)

	def _caclSliderValue(self, x):
		width = self.rect().width()
		left = self._handleOutterRadius
		right = width - self._handleOutterRadius
		rawValue = rangeMap(x, left, right, self.minValue, self.maxValue)
		if self.step:
			return round(rawValue / self.step) * self.step
		else:
			return rawValue

	def _updateValue(self, value):
		if self.value == value: return
		self.value = value
		self.update()

		currTime = time.time()
		if currTime > self.lastTriggerSignalTime + _valueUpdateInterval:
			self.valueChanged.emit(value)
			self.lastTriggerSignalTime = currTime

	def mousePressEvent(self, evt):
		x = evt.localPos().x()
		value = self._caclSliderValue(x)
		self._updateValue(value)
		self._updateState(SliderState.Pressed)
	def mouseReleaseEvent(self, evt):
		if self.state != SliderState.Pressed: return
		self._updateState(SliderState.Hovered)
	def mouseMoveEvent(self, evt):
		x = evt.localPos().x()
		value = self._caclSliderValue(x)
		self._updateValue(value)
		# self._updateState(SliderState.Pressed)