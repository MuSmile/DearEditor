from PySide6.QtCore import Qt, QRect, Property, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QPainterPath, QPen, QPalette
from PySide6.QtWidgets import QWidget
from editor.common.icon_cache import getThemePixmap
from editor.common.types import Color

class ReferenceEdit(QWidget):
	referenceChanged = Signal(str)

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

	@Property(QColor)
	def borderColor(self):
		return self._borderColor
	@borderColor.setter
	def borderColor(self, value):
		self._borderColor = value
	@Property(QColor)
	def borderColorHovered(self):
		return self._borderColorHovered
	@borderColorHovered.setter
	def borderColorHovered(self, value):
		self._borderColorHovered = value
	@Property(QColor)
	def borderColorFocused(self):
		return self._borderColorFocused
	@borderColorFocused.setter
	def borderColorFocused(self, value):
		self._borderColorFocused = value
	@Property(QColor)
	def borderColorReadonly(self):
		return self._borderColorReadonly
	@borderColorReadonly.setter
	def borderColorReadonly(self, value):
		self._borderColorReadonly = value
	@Property(int)
	def borderWidth(self):
		return self._penBorder.width() - 1
	@borderWidth.setter
	def borderWidth(self, value):
		self._penBorder.setWidth(value + 1)
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

	def __init__(self, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('color_picker.png')
		self._padding = 5

		self._borderColor = QColor('#222')
		self._borderColorHovered = QColor('#777')
		self._borderColorFocused = QColor('#5ae')
		self._borderColorReadonly = QColor('gray')
		self._borderRadius = 2
		self._penBorder = QPen(self._borderColor, 2)
		
		self.color = Color(180, 160, 200, 100)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.StrongFocus)

		self._btnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self._btnRect = QRect(w - h, 0, h, h)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		hover = self._btnRect.contains(evt.pos())
		if hover == self._btnHovered: return
		self._btnHovered = hover
		self.update()

	def mousePressEvent(self, evt):
		if self._btnHovered:
			print('>>>> pick reference')
		else:
			print('>>>> ping reference')

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
		rect = self.rect()
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.fillRect(QRect(0, 0, w - h, h), palette.color(QPalette.Base))
		
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(QRect(self._padding, 0, w - h - self._padding * 2, h), Qt.AlignVCenter, 'None (TextAsset)')

		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(3, 3, -3, -3), self._pixmapBtnIcon)

		if self.hasFocus():
			self._penBorder.setColor(self._borderColorFocused)
		elif self.underMouse():
			self._penBorder.setColor(self._borderColorHovered)
		else:
			self._penBorder.setColor(self._borderColor)

		painter.setPen(self._penBorder)
		painter.drawRoundedRect(rect, self._borderRadius, self._borderRadius)
