from enum import Enum
from PySide6.QtCore import Qt, QRect, Property
from PySide6.QtGui import QPainter, QPalette, QColor
from PySide6.QtWidgets import QWidget, QFrame, QStyleOptionFrame, QStyle

class Breadcrumb(QWidget):
	@Property(int)
	def spacing(self):
		return self._spacing
	@spacing.setter
	def spacing(self, value):
		self._spacing = value

	@Property(int)
	def paddingH(self):
		return self._paddingH
	@paddingH.setter
	def paddingH(self, value):
		self._paddingH = value
	@Property(int)
	def paddingV(self):
		return self._paddingV
	@paddingV.setter
	def paddingV(self, value):
		self._paddingV = value

	@Property(QColor)
	def highlightColor(self):
		return self._highlightColor
	@highlightColor.setter
	def highlightColor(self, value):
		self._highlightColor = value

	@Property(QColor)
	def separatorHoverColor(self):
		return self._separatorHoverColor
	@separatorHoverColor.setter
	def separatorHoverColor(self, value):
		self._separatorHoverColor = value

	def __init__(self, pathList, parent = None):
		super().__init__(parent)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.NoFocus)

		self._pathList = pathList
		self._nameRects = []
		self._separatorRects = []
		self._hoveredIndex = -1

		self._spacing  = 1
		self._paddingH = 4
		self._paddingV = 2
		self._highlightColor = QColor('#eee')
		self._separatorHoverColor = QColor('#888')

	def updateHovered(self, idx):
		if self._hoveredIndex == idx: return
		self._hoveredIndex = idx
		self.update()

	def resizeEvent(self, evt):
		spacing, paddingV = self._spacing, self._paddingV
		h = self.height() - paddingV * 2
		fm = self.fontMetrics()
		currx = self._paddingH
		for i in range(len(self._pathList) - 1):
			name = self._pathList[ i ]
			w = fm.horizontalAdvance(name)
			self._nameRects.append( QRect(currx, paddingV, w, h) )
			currx += w + spacing
			self._separatorRects.append( QRect(currx + 1, paddingV, h - 2, h - 1) )
			currx += h + spacing

		name = self._pathList[ -1 ]
		w = fm.horizontalAdvance(name)
		self._nameRects.append( QRect(currx, paddingV, w, h) )

	def mouseMoveEvent(self, evt):
		pos = evt.pos()
		for i in range(len(self._separatorRects)):
			if self._separatorRects[ i ].contains(pos):
				return self.updateHovered(i)
		self.updateHovered(-1)

	def leaveEvent(self, evt):
		self.updateHovered(-1)

	def mousePressEvent(self, evt):
		if self._hoveredIndex > -1:
			return print(f'press separator: {self._hoveredIndex}')

		pos = evt.pos()
		for i in range(len(self._nameRects)):
			rect = self._nameRects[ i ]
			if rect.contains(pos):
				return print(f'press name: {i}')

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		
		palette = self.palette()
		painter.fillRect(self.rect(), palette.color(QPalette.Base))
		
		count = len(self._pathList)
		textColor = palette.color(QPalette.Text)

		painter.setPen(textColor)
		for i in range(count - 1): painter.drawText(self._nameRects[ i ], Qt.AlignVCenter, self._pathList[ i ])
		painter.setPen(self._highlightColor)
		painter.drawText(self._nameRects[ -1 ], Qt.AlignVCenter, self._pathList[ -1 ])
		
		font = self.font()
		font.setPixelSize(font.pixelSize() + 2)
		painter.setFont(font)
		painter.setPen(textColor)
		flag = Qt.AlignCenter | Qt.AlignVCenter
		for i in range(count - 1):
			if self._hoveredIndex == i: continue
			painter.drawText(self._separatorRects[ i ], flag, '>')
		if self._hoveredIndex > -1:
			srect = self._separatorRects[ self._hoveredIndex ]
			painter.fillRect(srect, QColor('#888'))
			painter.setPen(self._highlightColor)
			painter.drawText(srect, flag, '>')

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		painter.setClipping(False)
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
