from PySide6.QtCore import Qt, Property, QRect
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QColor, QPixmap
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QStyle, QStyleOptionFrame
from editor.widgets.misc.collapsible import CollapsibleWidget
from editor.common.icon_cache import getThemePixmap

class FoldoutGroup(QWidget):
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

	@Property(QColor)
	def titleColor(self):
		return self._titleColor
	@titleColor.setter
	def titleColor(self, value):
		self._titleColor = value

	@Property(QColor)
	def separatorColor(self):
		return self._separatorColor
	@separatorColor.setter
	def separatorColor(self, value):
		self._separatorColor = value

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

	@Property(QPixmap)
	def pixmapGroupOpened(self):
		return self._pixmapGroupOpened
	@pixmapGroupOpened.setter
	def pixmapGroupOpened(self, value):
		self._pixmapGroupOpened = value
	@Property(QPixmap)
	def pixmapGroupClosed(self):
		return self._pixmapGroupClosed
	@pixmapGroupClosed.setter
	def pixmapGroupClosed(self, value):
		self._pixmapGroupClosed = value

	@Property(int)
	def groupIconSize(self):
		return self._groupIconSize
	@groupIconSize.setter
	def groupIconSize(self, value):
		self._groupIconSize = value

	def __init__(self, title, layout = None, parent = None):
		super().__init__(parent)
		self._title = title
		self._titleHeight = 22
		self._titlePadding = 0
		self._titleColor = QColor('#3a3a3a')
		self._separatorColor = QColor('#222')
		self._horizontalPadding = 0
		self._verticalPadding = 3
		self._borderRadius = 2

		self._groupIconSize = 14
		self._pixmapGroupOpened = getThemePixmap('arrow_down.png')
		self._pixmapGroupClosed = getThemePixmap('arrow_right.png')

		container = QWidget()
		collapsible = CollapsibleWidget()
		collapsible.setWidget(container)

		rootLayout = QVBoxLayout()
		rootLayout.setAlignment(Qt.AlignTop)
		rootLayout.setContentsMargins(self._horizontalPadding, self._titleHeight + self._verticalPadding, self._horizontalPadding, self._verticalPadding + 1)
		rootLayout.addWidget(collapsible)
		self.setLayout(rootLayout)

		if not layout: layout = QVBoxLayout()
		layout.setContentsMargins(0, 2, 0, 2)
		container.setLayout(layout)

		self.collapsible = collapsible
		self.container = container

	def updateFixedHeight(self):
		height = self.container.sizeHint().height()
		self.container.setFixedHeight(height)
		self.collapsible.setFixedHeight(height)

	def mousePressEvent(self, evt):
		pos = evt.pos()
		if pos.y() < self._titleHeight:
			self.collapsible.toggle()

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
		painter.fillRect(0, 0, w, self._titleHeight, self._titleColor)
		painter.fillRect(0, self._titleHeight - 1, w, 1, self._separatorColor)
		
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(self._titlePadding + self._groupIconSize + 1, 0, w - self._titlePadding * 2 -  + self._groupIconSize, self._titleHeight, Qt.AlignVCenter, self._title)
		pixmap = self._pixmapGroupOpened if self.collapsible._expanded else self._pixmapGroupClosed
		painter.drawPixmap(4, (self._titleHeight - self._groupIconSize) / 2, self._groupIconSize, self._groupIconSize, pixmap)

		painter.setClipping(False)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
