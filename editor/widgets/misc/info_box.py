from PySide6.QtCore import Qt, Property, QRect, QSize
from PySide6.QtGui import QPainter, QPainterPath, QPalette, QColor, QAction
from PySide6.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QStyle, QStyleOptionFrame
from editor.common.icon_cache import getThemePixmap

class InfoBox(QWidget):
	@Property(int)
	def iconSize(self):
		return self._iconSize
	@iconSize.setter
	def iconSize(self, value):
		self._iconSize = value

	@Property(int)
	def contentPadding(self):
		return self._contentPadding
	@contentPadding.setter
	def contentPadding(self, value):
		self._contentPadding = value

	@Property(int)
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value

	def __init__(self, text, level = None, parent = None):
		super().__init__(parent)
		self._text = text
		self._iconSize = 24
		self._borderRadius = 2
		self._contentPadding = 5
		self._textFlags = Qt.AlignVCenter | Qt.TextWordWrap

		if level == 'error':
			self._iconPixmap = getThemePixmap('error.png')
		elif level == 'warn':
			self._iconPixmap = getThemePixmap('warn.png')
		else:
			self._iconPixmap = getThemePixmap('info.png')

		copy = QAction('Copy message', self)
		copy.triggered.connect(self.copyMessage)
		self.addAction(copy)
		self.setContextMenuPolicy(Qt.ActionsContextMenu)

	def copyMessage(self):
		QApplication.clipboard().setText(self._text)

	def showEvent(self, evt):
		super().showEvent(evt)
		self.updateHeight()

	def resizeEvent(self, evt):
		super().resizeEvent(evt)
		self.updateHeight()

	def updateHeight(self):
		w = self.width() - self._iconSize - self._contentPadding * 3
		textRect = self.fontMetrics().boundingRect(0, 0, w, 0, self._textFlags, self._text)
		contentHeight = max(textRect.height(), self._iconSize)
		self.setFixedHeight(contentHeight + self._contentPadding * 2)

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

		painter.drawPixmap(self._contentPadding, (h - self._iconSize) / 2, self._iconSize, self._iconSize, self._iconPixmap)
		x = self._iconSize + self._contentPadding * 2
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(x, 0, w - x - self._contentPadding, h - 1, self._textFlags, self._text)

		painter.setClipping(False)
		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
