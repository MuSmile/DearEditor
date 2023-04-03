from PySide6.QtCore import Qt, QSize, QRect, Property, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QPen
from PySide6.QtWidgets import QWidget, QFrame, QStyleOptionFrame, QStyle
from editor.widgets.complex.color_picker import ColorPicker, ScreenColorPicker
from editor.common.icon_cache import getThemePixmap
from editor.common.types import Color

class ColorEdit(QWidget):
	colorChanged = Signal(Color)

	@Property(QColor)
	def buttonColor(self):
		return self._btnColor
	@buttonColor.setter
	def buttonColor(self, value):
		self._btnColor = value
	@Property(QColor)
	def buttonColorHovered(self):
		return self._btnColorHovered
	@buttonColorHovered.setter
	def buttonColorHovered(self, value):
		self._btnColorHovered = value

	@Property(QPixmap)
	def buttonIcon(self):
		return self._pixmapBtnIcon
	@buttonIcon.setter
	def buttonIcon(self, value):
		self._pixmapBtnIcon = value
		
	@Property(int)
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value
		
	@Property(int)
	def marginLeft(self):
		return self._marginLeft
	@marginLeft.setter
	def marginLeft(self, value):
		self._marginLeft = value
	@Property(int)
	def marginRight(self):
		return self._marginRight
	@marginRight.setter
	def marginRight(self, value):
		self._marginRight = value

	def __init__(self, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('color_picker.png')
		self._borderRadius = 2
		self._marginLeft = 0
		self._marginRight = 0
		
		self.color = Color(180, 160, 200, 100)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.StrongFocus)

		self._btnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self._btnRect = QRect(w - h - self._marginRight, 0, h, h)
		# self.setStyleSheet(f'ColorEdit{{ padding-right: {h}px; }}')

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		hover = self._btnRect.contains(evt.pos())
		if hover == self._btnHovered: return
		self._btnHovered = hover
		self.update()

	def mousePressEvent(self, evt):
		if self._btnHovered:
			def onColorPick(color, picked):
				a = self.color.raw.alpha()
				self.color.raw = color
				self.color.raw.setAlpha(a)
				self.update()
			ScreenColorPicker.showScreenColorPicker(self.color.raw, onColorPick)
		else:
			def onColorPick(color, reason):
				self.color.raw = color
				self.update()
			colorPicker = ColorPicker(self.color.raw)
			colorPicker.colorChanged.connect(onColorPick)
			colorPicker.show()
	
	def keyPressEvent(self, evt):
		ScreenColorPicker.redirectKeyPressEvent(evt)

	def enterEvent(self, evt):
		super().enterEvent(evt)
		self.update()

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		self._btnHovered = False
		self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		rect = self.rect().adjusted(self._marginLeft, 0, -self._marginRight, 0)
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		
		x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
		alphaH = 4 # round(h * 0.22)
		colorW = w - h
		preview = QColor(self.color.raw)
		preview.setAlphaF(1)
		painter.fillRect(QRect(self._marginLeft, 0, colorW, h - alphaH), preview)
		alphaW = round(self.color.raw.alphaF() * colorW)
		painter.fillRect(QRect(self._marginLeft, h - alphaH, alphaW, alphaH), Qt.white)
		painter.fillRect(QRect(alphaW + 1, h - alphaH, colorW - alphaW, alphaH), Qt.black)

		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(3, 3, -3, -3), self._pixmapBtnIcon)

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)

	def minimumSizeHint(self):
		return QSize(180, 20)
