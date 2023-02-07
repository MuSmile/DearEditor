from PySide6.QtCore import Qt, QRect, Property
from PySide6.QtGui import QGuiApplication, QCursor, QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QLineEdit
from editor.tools.icon_cache import getThemePixmap

class SearchField(QLineEdit):
	def __init__(self,  parent=None):
		super().__init__(parent)

		self._pixmapSearch = getThemePixmap('search.png')
		# self._pixmapClear  = getThemePixmap('close.png')

		self.margin = 4
		self.setContentsMargins(self.margin, 0, self.margin, 0)
		self.textChanged.connect(self.onTextChange)
		self.returnPressed.connect(self.clearFocus)

		self.showClearButton = False
		self.hoverClearButton = False
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.ClickFocus)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self.searchRect = QRect(self.margin, 0, h, h)
		self.closeRect = QRect(w - h - self.margin, 0, h, h)
		self.searchRect.adjust(2, 2, -2, -2)
		self.closeRect.adjust(2, 2, -2, -2)

	def onTextChange(self):
		showClearBtn = bool(self.text())
		if self.showClearButton != showClearBtn:
			self.showClearButton = showClearBtn
			self.update()

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.clear()
			self.clearFocus()
		else:
			super().keyPressEvent(evt)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		if not self.showClearButton: return
		hover = self.closeRect.contains(evt.pos())
		if hover == self.hoverClearButton: return
		if hover:
			QGuiApplication.setOverrideCursor(Qt.ArrowCursor)
		else:
			QGuiApplication.restoreOverrideCursor()
		self.hoverClearButton = hover

	def mousePressEvent(self, evt):
		super().mousePressEvent(evt)
		if self.hoverClearButton:
			self.clear()
			QGuiApplication.restoreOverrideCursor()

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		if self.hoverClearButton: QGuiApplication.restoreOverrideCursor()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.drawPixmap(self.searchRect, self._pixmapSearch)
		if self.showClearButton:
			# painter.drawPixmap(self.closeRect, self._pixmapClear)
			painter.setPen(QPen(QColor(200, 200, 200), 1.5))
			rect = self.closeRect.adjusted(4, 4, -4, -4)
			painter.drawLine(rect.topLeft(), rect.bottomRight())
			painter.drawLine(rect.topRight(), rect.bottomLeft())

	@Property(QPixmap)
	def searchIcon(self):
		return self._pixmapSearch
	@searchIcon.setter
	def searchIcon(self, value):
		self._pixmapSearch = value
		self.update()

	# @Property(QPixmap)
	# def clearIcon(self):
	# 	return self._pixmapClear
	# @clearIcon.setter
	# def clearIcon(self, value):
	# 	self._pixmapClear = value
	# 	self.update()
