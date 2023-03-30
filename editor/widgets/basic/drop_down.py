from PySide6.QtCore import Qt, Property, QSize, QRect, QEvent, QTimer
from PySide6.QtGui import QPixmap, QPainter, QCursor, QColor, QPen, QPainterPath, QPalette, QCursor
from PySide6.QtWidgets import QPushButton, QWidget, QFrame, QScrollBar, QStyleOptionFrame, QStyle, QVBoxLayout, QSizePolicy
from editor.widgets.basic.line_edit import SearchLineEdit
from editor.common.icon_cache import getThemePixmap
from editor.common.util import adjustedPopupPosition, fuzzyContains
from math import floor

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

	def showPopup(self):
		self.popup = DropDownPopup(self)
		self.popup.show() # need show before resize, for updating popup's child widgets
		self.popup.resize(self.width(), self.popup.sizeHint().height())

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
	@Property(int)
	def itemHeight(self):
		return self._itemHeight
	@itemHeight.setter
	def itemHeight(self, value):
		self._itemHeight = value
	@Property(QColor)
	def itembackgroundHovered(self):
		return self._itembackgroundHovered
	@itembackgroundHovered.setter
	def itembackgroundHovered(self, value):
		self._itembackgroundHovered = value
	@Property(int)
	def itemBackgroundPadding(self):
		return self._itemBackgroundPadding
	@itemBackgroundPadding.setter
	def itemBackgroundPadding(self, value):
		self._itemBackgroundPadding = value
	@Property(int)
	def itemBackgroundRadius(self):
		return self._itemBackgroundRadius
	@itemBackgroundRadius.setter
	def itemBackgroundRadius(self, value):
		self._itemBackgroundRadius = value

	@Property(QPixmap)
	def itemIcon(self):
		return self._itemIcon
	@itemIcon.setter
	def itemIcon(self, value):
		self._itemIcon = value
	@Property(int)
	def itemIconSize(self):
		return self._itemIconSize
	@itemIconSize.setter
	def itemIconSize(self, value):
		self._itemIconSize = value

	@Property(int)
	def textPadding(self):
		return self._textPadding
	@textPadding.setter
	def textPadding(self, value):
		self._textPadding = value
	@Property(int)
	def iconPadding(self):
		return self._iconPadding
	@iconPadding.setter
	def iconPadding(self, value):
		self._iconPadding = value
	@Property(int)
	def verticalPadding(self):
		return self._verticalPadding
	@verticalPadding.setter
	def verticalPadding(self, value):
		self._verticalPadding = value

	@Property(int)
	def visibleCount(self):
		return self._visibleCount
	@visibleCount.setter
	def visibleCount(self, value):
		self._visibleCount = value
		if self.scrollBar:
			count = len(self.items()) - value
			self.scrollBar.setRange(0, count * self._itemHeight)

	def __init__(self, parent):
		super().__init__(parent)
		self.setWindowFlag(Qt.Popup, True)
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.setWindowFlag(Qt.NoDropShadowWindowHint, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setMouseTracking(True)

		self._itemHeight = 22;
		self._itembackgroundHovered = QColor('#47f')
		self._itemBackgroundPadding = 5
		self._itemBackgroundRadius = 4
		self._itemIcon = getThemePixmap('check2.png')
		self._itemIconSize = 12
		self._textPadding = 27
		self._iconPadding = 10
		self._verticalPadding = 4
		self._visibleCount = 20

		self._filteredItems = None
		self._hoveredIndex = None
		self._aboutToClose = False
		self._showAtAbove = None

		self.searchEdit = None
		self.scrollBar = None

		itemCount = len(self.rawItems())
		if itemCount > self._visibleCount:
			self.scrollBar = QScrollBar(Qt.Vertical, self)
			self.scrollBar.setSingleStep(self._itemHeight // 2)
			self.scrollBar.setPageStep(self._visibleCount * self._itemHeight)
			self.scrollBar.setRange(0, (itemCount - self._visibleCount) * self._itemHeight)
			self.scrollBar.valueChanged.connect(self.update)

			self.searchEdit = SearchLineEdit(self)
			self.searchEdit.setContentsMargins(4, 3, 4, 3)
			self.searchEdit.setFocus()
			self.searchEdit.textChanged.connect(self.setFilter)

			parent.window().installEventFilter(self.searchEdit)
			self.searchEdit.installEventFilter(self)

	def setFilter(self, text):
		if not text: self._filteredItems = None
		else: self._filteredItems = [item for item in self.rawItems() if fuzzyContains(item, text)]
		itemCount = len(self.items())
		if itemCount > self._visibleCount:
			self.scrollBar.setRange(0, (itemCount - self._visibleCount) * self._itemHeight)
			self.scrollBar.show()
		else:
			self.scrollBar.setRange(0, 0)
			self.scrollBar.hide()
		self.resize(self.sizeHint())
		pos = self.mapFromGlobal(QCursor.pos())
		self.calcCurrentHovered(pos)
		self.update()
	def isFiltered(self):
		return self._filteredItems != None
	def filteredIdxToRawIdx(self, idx):
		if idx == None: return idx
		if self.isFiltered(): return self.rawItems().index(self._filteredItems[ idx ])
		return idx

	def items(self):
		return self._filteredItems if self.isFiltered() else self.rawItems()
	def rawItems(self):
		return self.parent()._items

	def scrollPos(self):
		return self.scrollBar.value() if self.scrollBar else 0
	def searchEditHeight(self):
		return self.searchEdit.height() if self.searchEdit else 0

	def resizeEvent(self, evt):
		super().resizeEvent(evt)
		if self.scrollBar:
			sh = self.searchEditHeight()
			w = self.scrollBar.width()
			h = self.height() - sh
			self.scrollBar.move(self.width() - w, sh)
			self.scrollBar.setFixedHeight(h)
		if self.searchEdit:
			self.searchEdit.setFixedWidth(self.width())

		parent = self.parent()
		self.move(adjustedPopupPosition(parent, self.width(), self.height(), self._showAtAbove))
		if self._showAtAbove == None: self._showAtAbove = self.y() < parent.y()

	def mouseMoveEvent(self, evt):
		if self._aboutToClose: return
		self.calcCurrentHovered(evt.pos())

	def mouseReleaseEvent(self, evt):
		if self._aboutToClose: return
		if self._hoveredIndex == None: return self.close()
		self.playClickEffect()

	def wheelEvent(self, evt):
		if self._aboutToClose: return
		if not self.scrollBar: return
		self.scrollBar.wheelEvent(evt)
		pos = self.mapFromGlobal(QCursor.pos())
		self.calcCurrentHovered(pos)

	def eventFilter(self, obj, evt):
		if evt.type() == QEvent.KeyPress:
			if evt.key() == Qt.Key_Escape:
				self.close()
		return False

	def calcCurrentHovered(self, pos):
		x, y = pos.x(), pos.y()
		rect = self.rect()
		sp = self.scrollPos()
		sh = self.searchEditHeight()

		hovered = None
		right = self.scrollBar.x() if self.scrollBar and self.scrollBar.isVisible() else rect.right()
		checkX = rect.left() <= x and x <= right
		checkY = sh + self._verticalPadding <= y and y < rect.bottom() - self._verticalPadding - 1
		if checkX and checkY: hovered = (y - sh + sp - self._verticalPadding) // self._itemHeight
		self.updateHovered(hovered)

	def updateHovered(self, hovered):
		if self._hoveredIndex != hovered:
			self._hoveredIndex = hovered
			self.update()

	def closeAndSyncHovered(self):
		idx = self.filteredIdxToRawIdx(self._hoveredIndex)
		self.parent().setCurrentIndex(idx)
		self.close()

	def playClickEffect(self):
		hovered = self._hoveredIndex
		self.updateHovered(None)
		QTimer.singleShot(40, lambda: self.updateHovered(hovered))
		QTimer.singleShot(70, self.closeAndSyncHovered)
		self._aboutToClose = True

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		style = self.style()
		style.drawPrimitive(QStyle.PE_Widget, option, painter, self)
		style.drawPrimitive(QStyle.PE_Frame, option, painter, self)
		
		sp = self.scrollPos()
		sh = self.searchEditHeight()

		items = self.items()
		rawItems = self.rawItems()
		count = min(len(items), self._visibleCount)
		if sp % self._itemHeight != 0: count += 1

		rect = self.rect()
		painter.setClipRect(rect.adjusted(0, sh + 1, 0, -2))

		startIdx = sp // self._itemHeight
		currIdx = self.parent()._currentIndex
		textColor = self.palette().color(QPalette.Text)
		for i in range(startIdx, startIdx + count):
			idx = self.filteredIdxToRawIdx(i)
			itemRect = QRect(0, sh + i * self._itemHeight + self._verticalPadding - sp, rect.width(), self._itemHeight)
			if self.scrollBar and self.scrollBar.isVisible(): itemRect.setRight(itemRect.right() - self.scrollBar.width())

			if self._hoveredIndex == i:
				bgRect = itemRect.adjusted(self._itemBackgroundPadding, 0, -self._itemBackgroundPadding, 0)
				painter.setPen(Qt.transparent)
				painter.setBrush(self._itembackgroundHovered)
				painter.drawRoundedRect(bgRect, self._itemBackgroundRadius, self._itemBackgroundRadius)

			if currIdx == idx:
				cy = itemRect.center().y()
				iconRect = QRect(self._iconPadding, cy - self._itemIconSize // 2 + 1, self._itemIconSize, self._itemIconSize)
				painter.drawPixmap(iconRect, self._itemIcon)

			textRect = itemRect.adjusted(self._textPadding, 0, -self._textPadding, 0)
			painter.setPen(textColor)
			painter.drawText(textRect, Qt.AlignVCenter, items[i])

		painter.setClipping(False)
		painter.setPen(QColor('#222'))
		painter.drawLine(1, sh, self.width()-1, sh)

	def sizeHint(self):
		items = self.items()
		return QSize(self.parent().width(), self.searchEditHeight() + min(len(items), self._visibleCount) * self._itemHeight + self._verticalPadding * 2 + 1)

class FlagDropDown(DropDown):
	def allIndex(self):
		return pow(2, len(self._items)) - 1

	def updateText(self):
		idx = self._currentIndex
		if idx == 0:
			self.setText('None')
		elif idx == self.allIndex():
			self.setText('All')
		else:
			flaggeds = [self._items[i] for i in range(len(self._items)) if idx & 1 << i]
			if len(flaggeds) > 2: flaggeds = flaggeds[:2] + ['...']
			self.setText(', '.join(flaggeds))

	def setCurrentIndex(self, index):
		# if self._currentIndex == index: return
		self._currentIndex = index
		if not self._items: return
		allIdx = self.allIndex()
		if index < 0: self._currentIndex = allIdx
		self.updateText()

	def setFlag(self, item, flagged):
		idx = self._items.index(item)
		self.setFlagAt(idx, flagged)
	def setFlagAt(self, idx, flagged):
		if idx < 0: return
		if flagged: self._currentIndex |= 1 << idx
		else: self._currentIndex &= ~(1 << idx)
		self.updateText()

	def toggleFlag(self, item):
		idx = self._items.index(item)
		self.toggleFlagAt(idx)
	def toggleFlagAt(self, idx):
		if idx < 0: return
		self._currentIndex ^= 1 << idx
		self.updateText()

	def showPopup(self):
		self.popup = FlagDropDownPopup(self)
		self.popup.show() # need show before resize, for updating popup's child widgets
		self.popup.resize(self.width(), self.popup.sizeHint().height())

class FlagDropDownPopup(DropDownPopup):
	@Property(QColor)
	def itemIndicatorColor(self):
		return self._itemIndicatorColor
	@itemIndicatorColor.setter
	def itemIndicatorColor(self, value):
		self._itemIndicatorColor = value
	@Property(int)
	def itemIndicatorPadding(self):
		return self._itemIndicatorPadding
	@itemIndicatorPadding.setter
	def itemIndicatorPadding(self, value):
		self._itemIndicatorPadding = value

	def __init__(self, parent):
		self._items = [ 'None' ]
		self._items.extend(parent._items)
		self._items.append('All')

		super().__init__(parent)
		self._itemIndicatorColor = QColor('#00c700')
		self._itemIndicatorPadding = 2

	def rawItems(self):
		return self._items

	def mousePressEvent(self, evt):
		if self._hoveredIndex == None: return self.close()
		dropdown = self.parent()
		idx = self.filteredIdxToRawIdx(self._hoveredIndex)
		if idx == 0:
			dropdown.setCurrentIndex(0)
		elif idx == len(self._items) - 1:
			if dropdown._currentIndex == dropdown.allIndex():
				dropdown.setCurrentIndex(0)
			else:
				dropdown.setCurrentIndex(-1)
		else:
			dropdown.toggleFlagAt(idx - 1)
		self.update()
	def mouseReleaseEvent(self, evt):
		pass

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		style = self.style()
		style.drawPrimitive(QStyle.PE_Widget, option, painter, self)
		style.drawPrimitive(QStyle.PE_Frame, option, painter, self)
		
		sp = self.scrollPos()
		sh = self.searchEditHeight()

		items = self.items()
		count = min(len(items), self._visibleCount)
		rawItems = self.rawItems()
		rawCount = len(rawItems)
		if sp % self._itemHeight != 0: count += 1

		rect = self.rect()
		painter.setClipRect(rect.adjusted(0, sh + 1, 0, -2))

		startIdx = sp // self._itemHeight
		currIdx = self.parent()._currentIndex
		textColor = self.palette().color(QPalette.Text)
		hovered = self.filteredIdxToRawIdx(self._hoveredIndex)
		for i in range(startIdx, startIdx + count):
			idx = self.filteredIdxToRawIdx(i)
			itemRect = QRect(0, sh + i * self._itemHeight + self._verticalPadding - sp, rect.width(), self._itemHeight)
			if self.scrollBar and self.scrollBar.isVisible(): itemRect.setRight(itemRect.right() - self.scrollBar.width())

			if self._hoveredIndex == i:
				bgRect = itemRect.adjusted(self._itemBackgroundPadding, 0, -self._itemBackgroundPadding, 0)
				painter.setPen(Qt.transparent)
				painter.setBrush(self._itembackgroundHovered)
				painter.drawRoundedRect(bgRect, self._itemBackgroundRadius, self._itemBackgroundRadius)
			
			if hovered == rawCount - 1 and 0 < idx and idx < rawCount - 1:
				padding = self._itemIndicatorPadding
				x, y, h = itemRect.x(), itemRect.y(), itemRect.height()
				indicatorRect = QRect(x + padding, y + padding, 2, h - padding * 2)
				painter.fillRect(indicatorRect, self._itemIndicatorColor)

			if idx < rawCount - 1:
				cy = itemRect.center().y()
				size = self._itemIconSize
				iconRect = QRect(self._iconPadding, cy - size // 2 + 1, size, size)
				checked = (idx == 0 and currIdx == 0) or (idx > 0 and currIdx & 1 << (idx - 1))
				if checked:
					painter.drawPixmap(iconRect, self._itemIcon)
				else:
					painter.setPen(Qt.gray)
					painter.setBrush(Qt.transparent)
					painter.drawEllipse(iconRect.adjusted(1, 1, -1, -1))

			textRect = itemRect.adjusted(self._textPadding, 0, -self._textPadding, 0)
			painter.setPen(textColor)
			painter.drawText(textRect, Qt.AlignVCenter, items[i])

		painter.setClipping(False)
		painter.setPen(QColor('#222'))
		painter.drawLine(1, sh, self.width()-1, sh)
