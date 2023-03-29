from PySide6.QtCore import Qt, Property, QSize, QRect
from PySide6.QtGui import QPixmap, QPainter, QCursor, QColor, QPen, QPainterPath, QPalette
from PySide6.QtWidgets import QPushButton, QWidget, QFrame, QStyleOptionFrame, QStyle, QVBoxLayout, QSizePolicy
from editor.widgets.basic.line_edit import SearchLineEdit
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

	def setItems(self, items):
		self._items = items

	def setCurrentIndex(self, index):
		if self._currentIndex == index: return
		self._currentIndex = index
		if not self._items: return
		if index < 0 and index >= len(self._items): return
		self.setText(self._items[index])

	def setCurrentItem(self, item):
		self.setCurrentIndex(self._items.index(item))

	def showPopup(self):
		self.popup = DropDownPopup(self._items, self)
		self.popup.show()
		self.popup.resize(self.width(), self.popup.sizeHint().height())
		pos = adjustedPopupPosition(self, self.width(), self.popup.height())
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
	def __init__(self, items, parent):
		super().__init__(parent)
		self.setWindowFlag(Qt.Popup, True)
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.setWindowFlag(Qt.NoDropShadowWindowHint, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

		self._items = items
		self._itemHeight = 22;
		self._backgroundHovered = QColor('#47f')
		self._itemBackgroundPadding = 5
		self._itemBackgroundRadius = 4
		self._itemIcon = getThemePixmap('check2.png')
		self._itemIconSize = 12
		self._textPadding = 25
		self._iconPadding = 10

		self.searchEdit = SearchLineEdit(self)
		self.searchEdit.setContentsMargins(4, 3, 4, 3)
		self.searchEdit.setFocus()
		parent.installEventFilter(self.searchEdit)
		self.setMouseTracking(True)

	def resizeEvent(self, evt):
		super().resizeEvent(evt)
		self.searchEdit.setFixedWidth(self.width())

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		# print('move')

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		style = self.style()
		style.drawPrimitive(QStyle.PE_Widget, option, painter, self)
		style.drawPrimitive(QStyle.PE_Frame, option, painter, self)
		
		sh = self.searchEdit.height()
		painter.setPen(QColor('#333'))
		painter.drawLine(1, sh, self.width()-1, sh)

		# painter.setPen(self.palette().color(QPalette.Text))
		for i in range(len(self._items)):
			# painter.setPen(QColor('#333'))
			# painter.drawLine(1, sh + i * self._itemHeight, self.width()-1, sh + i * self._itemHeight)
			# painter.setPen(self.palette().color(QPalette.Text))
			rect = QRect(0, sh + i * self._itemHeight, self.width(), self._itemHeight)
			# painter.setBrush(self._backgroundHovered)
			# painter.setPen(Qt.transparent)
			# painter.drawRoundedRect(rect.adjusted(self._itemBackgroundPadding, 0, -self._itemBackgroundPadding, 0), self._itemBackgroundRadius, self._itemBackgroundRadius)

			cy = rect.center().y()
			iconRect = QRect(self._iconPadding, cy - self._itemIconSize // 2 + 1, self._itemIconSize, self._itemIconSize)
			painter.drawPixmap(iconRect, self._itemIcon)
			painter.setPen(self.palette().color(QPalette.Text))
			painter.drawText(self._textPadding, sh + i * self._itemHeight, self.width() - self._textPadding * 2, self._itemHeight, Qt.AlignVCenter, self._items[i])

	def sizeHint(self):
		return QSize(self.parent().width(), self.searchEdit.height() + len(self._items) * self._itemHeight + 2)
