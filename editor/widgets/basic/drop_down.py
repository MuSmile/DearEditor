from PySide6.QtCore import Qt, Property, QRect
from PySide6.QtGui import QPixmap, QPainter, QCursor, QColor, QPen, QPainterPath
from PySide6.QtWidgets import QPushButton, QWidget, QFrame, QStyleOptionFrame, QStyle
from editor.common.icon_cache import getThemePixmap
from editor.common.util import adjustedPopupPosition

class DropDown(QPushButton):
	@Property(QPixmap)
	def menuIndicator(self):
		return self._menuIndicator
	@menuIndicator.setter
	def menuIndicator(self, value):
		self._menuIndicator = value

	@Property(int)
	def menuIndicatorSize(self):
		return self._menuIndicatorSize
	@menuIndicatorSize.setter
	def menuIndicatorSize(self, value):
		self._menuIndicatorSize = value

	@Property(int)
	def menuIndicatorOffsetX(self):
		return self._menuIndicatorOffsetX
	@menuIndicatorOffsetX.setter
	def menuIndicatorOffsetX(self, value):
		self._menuIndicatorOffsetX = value
	@Property(int)
	def menuIndicatorOffsetY(self):
		return self._menuIndicatorOffsetY
	@menuIndicatorOffsetY.setter
	def menuIndicatorOffsetY(self, value):
		self._menuIndicatorOffsetY = value


	def __init__(self, parent = None):
		super().__init__(parent)
		self._items = None
		self._currentIndex = 0
		self._menuIndicator = getThemePixmap('menu_indicator.svg')
		self._menuIndicatorSize = 16
		self._menuIndicatorOffsetX = -5
		self._menuIndicatorOffsetY = 1

		self.clicked.connect(self.showPopup)

	def addItems(self, items):
		self._items = items

	def setCurrentIndex(self, index):
		self._currentIndex = index
		if not self._items: return
		if index < 0 and index >= len(self._items): return
		self.setText(self._items[index])

	def showPopup(self):
		self.popup = DropDownPopup(True, self)
		self.popup.show()
		self.popup.resize(self.width(), 200)
		pos = adjustedPopupPosition(self, self.width(), 200)
		self.popup.move(pos)

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		rect = self.rect()
		y, r = rect.center().y(), rect.right()
		size = self._menuIndicatorSize
		offsetX = self._menuIndicatorOffsetX
		offsetY = self._menuIndicatorOffsetY
		iconRect = QRect(r - size + offsetX, y - size // 2 + offsetY, size, size)
		painter.drawPixmap(iconRect, self._menuIndicator)

class DropDownPopup(QWidget):
	def __init__(self, searchable, parent):
		super().__init__(parent)
		self.setWindowFlag(Qt.Popup, True)
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.setWindowFlag(Qt.NoDropShadowWindowHint, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		style = self.style()
		style.drawPrimitive(QStyle.PE_Widget, option, painter, self)
		style.drawPrimitive(QStyle.PE_Frame, option, painter, self)
