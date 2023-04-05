from PySide6.QtCore import Qt, Property, QRect
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QColor
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QStyle, QStyleOptionFrame

class BoxGroup(QWidget):
	@Property(int)
	def titleHeight(self):
		return self._titleHeight
	@titleHeight.setter
	def titleHeight(self, value):
		self._titleHeight = value
	@Property(int)
	def titlePadding(self):
		return self._titlePadding
	@titlePadding.setter
	def titlePadding(self, value):
		self._titlePadding = value

	@Property(int)
	def horizontalPadding(self):
		return self._horizontalPadding
	@horizontalPadding.setter
	def horizontalPadding(self, value):
		self._horizontalPadding = value
		self.layout().setContentsMargins(value, self._titleHeight + self._verticalPadding, value, self._verticalPadding + 1)
	@Property(int)
	def verticalPadding(self):
		return self._verticalPadding
	@verticalPadding.setter
	def verticalPadding(self, value):
		self._verticalPadding = value
		self.layout().setContentsMargins(self._horizontalPadding, self._titleHeight + value, self._horizontalPadding, value + 1)

	@Property(int)
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value

	def __init__(self, title, layout = None, parent = None):
		super().__init__(parent)
		self._title = title
		self._titleHeight = 22
		self._titlePadding = 0
		self._horizontalPadding = 0
		self._verticalPadding = 3
		self._borderRadius = 2

		if not layout: layout = QVBoxLayout()
		layout.setContentsMargins(self._horizontalPadding, self._titleHeight + self._verticalPadding, self._horizontalPadding, self._verticalPadding + 1)
		self.setLayout(layout)

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)

		rect = self.rect()
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.fillRect(rect, palette.color(QPalette.Base))
		painter.fillRect(0, 0, w, self._titleHeight, QColor('#3a3a3a'))
		
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(self._titlePadding, 0, w - self._titlePadding * 2, self._titleHeight, Qt.AlignVCenter, self._title)

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
