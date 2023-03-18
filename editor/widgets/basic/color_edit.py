from PySide6.QtCore import Qt, QRect, Property, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath
from PySide6.QtWidgets import QFrame
from editor.common.icon_cache import getThemePixmap
from editor.common.types import Color

class ColorEdit(QFrame):
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
	def buttonRadius(self):
		return self._btnRadius
	@buttonRadius.setter
	def buttonRadius(self, value):
		self._btnRadius = value

	def __init__(self, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('color_picker.png')
		self._btnRadius = 2
		
		self.color = Color(180, 160, 200, 100)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.StrongFocus)

		self._btnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self._btnRect = QRect(w - h, 0, h, h)
		# self.setStyleSheet(f'ColorEdit{{ padding-right: {h}px; }}')

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		hover = self._btnRect.contains(evt.pos())
		if hover == self._btnHovered: return
		self._btnHovered = hover
		self.update()

	def mousePressEvent(self, evt):
		if self._btnHovered:
			print('>>>> pick screen color')
		else:
			print('>>>> open color picker')

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		self._btnHovered = False
		self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		rect = self.rect()
		path = QPainterPath()
		radius = max(self._btnRadius - 1, 0)
		path.addRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)
		painter.setClipPath(path)
		
		x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
		alphaH = 4 # round(h * 0.22)
		colorW = w - h
		preview = QColor(self.color.r, self.color.g, self.color.b)
		painter.fillRect(QRect(0, 0, colorW, h - alphaH), preview)
		alphaW = round(self.color.alphaF() * colorW)
		painter.fillRect(QRect(0, h - alphaH, alphaW, alphaH), Qt.white)
		painter.fillRect(QRect(alphaW + 1, h - alphaH, colorW - alphaW, alphaH), Qt.black)

		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(3, 3, -3, -3), self._pixmapBtnIcon)

