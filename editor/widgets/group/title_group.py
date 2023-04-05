from PySide6.QtCore import Qt, Property
from PySide6.QtGui import QPainter, QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout

class TitleGroup(QWidget):
	@Property(int)
	def separatorHeight(self):
		return self._separatorHeight
	@separatorHeight.setter
	def separatorHeight(self, value):
		self._separatorHeight = value

	@Property(int)
	def titlePadding(self):
		return self._titlePadding
	@titlePadding.setter
	def titlePadding(self, value):
		self._titlePadding = value

	@Property(int)
	def titleAlignment(self):
		return self._titleAlignment
	@titleAlignment.setter
	def titleAlignment(self, value):
		self._titleAlignment = value

	@Property(int)
	def titleSpacing(self):
		return self._titleSpacing
	@titleSpacing.setter
	def titleSpacing(self, value):
		self._titleSpacing = value

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

	def __init__(self, title, layout = None, parent = None):
		super().__init__(parent)
		self._title = title
		self._titlePadding = 2
		self._titleAlignment = Qt.AlignHCenter
		self._separatorHeight = 1
		self._titleSpacing = 4
		self._marginLeft = 0
		self._marginRight = 0

		if not layout: layout = QVBoxLayout()
		self._titleHeight = self.fontMetrics().height()
		layout.setContentsMargins(0, self._titleHeight + self._titleSpacing * 2 + self._separatorHeight, 0, 0)
		self.setLayout(layout)

	def setHorizontalMargins(self, marginLeft, marginRight):
		self._marginLeft = marginLeft
		self._marginRight = marginRight

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)

		titleHeight = self.fontMetrics().height()
		if self._titleHeight != titleHeight:
			self._titleHeight = titleHeight
			self.layout().setContentsMargins(0, titleHeight + self._titleSpacing * 2 + self._separatorHeight, 0, 0)
		
		palette = self.palette()
		w, h = self.width(), self.height()
		ml, mw = self._marginLeft, self._marginLeft + self._marginRight
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(ml + self._titlePadding, 0, w - self._titlePadding * 2 - mw, titleHeight, self._titleAlignment | Qt.AlignTop, self._title)
		painter.fillRect(ml, titleHeight + self._titleSpacing, w - mw, self._separatorHeight, palette.color(QPalette.Base))
