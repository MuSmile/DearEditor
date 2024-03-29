from PySide6.QtCore import Qt, QSize, QRect, Property, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QPen, QPalette
from PySide6.QtWidgets import QWidget, QFrame, QStyleOptionFrame, QStyle
from editor.common.icon_cache import getThemePixmap
from editor.common.types import Color

class ObjectEdit(QWidget):
	objectChanged = Signal(str)

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
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value

	@Property(int)
	def padding(self):
		return self._padding
	@padding.setter
	def padding(self, value):
		self._padding = value
		
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

	def __init__(self, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('color_picker.png')
		self._borderRadius = 2
		self._padding = 5
		self._marginLeft = 0
		self._marginRight = 0
		
		self.color = Color(180, 160, 200, 100)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.StrongFocus)

		self._btnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self._btnRect = QRect(w - h - self._marginRight, 0, h, h)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		hover = self._btnRect.contains(evt.pos())
		if hover == self._btnHovered: return
		self._btnHovered = hover
		self.update()

	def mousePressEvent(self, evt):
		if self._btnHovered:
			print('>>>> pick object')
		else:
			print('>>>> ping object')

	def enterEvent(self, evt):
		super().enterEvent(evt)
		self.update()

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		self._btnHovered = False
		self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		rect = self.rect().adjusted(self._marginLeft, 0, -self._marginRight, 0)
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.fillRect(QRect(self._marginLeft, 0, w - h, h), palette.color(QPalette.Base))
		
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(QRect(self._marginLeft + self._padding, 0, w - h - self._padding * 2, h), Qt.AlignVCenter, 'None (TextAsset)')

		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(2, 2, -2, -2), self._pixmapBtnIcon)

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		painter.setClipping(False)
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)

	def minimumSizeHint(self):
		return QSize(180, 20)
		