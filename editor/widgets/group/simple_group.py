from PySide6.QtCore import Qt, Property, QRect, QSize
from PySide6.QtGui import QPainter, QPalette, QColor, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout
from editor.widgets.misc.collapsible import CollapsibleWidget
from editor.common.icon_cache import getThemePixmap

class SimpleGroup(QWidget):
	@Property(int)
	def titleHeight(self):
		return self._titleHeight
	@titleHeight.setter
	def titleHeight(self, value):
		self._titleHeight = value
		self.layout().setContentsMargins(self._contentIndention, value, 0, 0)

	@Property(int)
	def contentIndention(self):
		return self._contentIndention
	@contentIndention.setter
	def contentIndention(self, value):
		self._contentIndention = value
		self.layout().setContentsMargins(value, self._titleHeight, 0, 0)

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
		self._contentIndention = 24
		self._groupIconSize = 14
		self._pixmapGroupOpened = getThemePixmap('arrow_down.png')
		self._pixmapGroupClosed = getThemePixmap('arrow_right.png')

		container = QWidget()
		collapsible = CollapsibleWidget()
		collapsible.setWidget(container)

		rootLayout = QVBoxLayout()
		rootLayout.setAlignment(Qt.AlignTop)
		rootLayout.setContentsMargins(self._contentIndention, self._titleHeight, 0, 0)
		rootLayout.addWidget(collapsible)
		self.setLayout(rootLayout)

		if not layout: layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
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
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)

		rect = self.rect()
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(self._groupIconSize + 2, 0, w - self._groupIconSize, self._titleHeight, Qt.AlignVCenter, self._title)
		pixmap = self._pixmapGroupOpened if self.collapsible._expanded else self._pixmapGroupClosed
		painter.drawPixmap(0, (self._titleHeight - self._groupIconSize) / 2, self._groupIconSize, self._groupIconSize, pixmap)
