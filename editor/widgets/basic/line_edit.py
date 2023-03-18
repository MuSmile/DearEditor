import os
from PySide6.QtCore import Qt, QRect, Property
from PySide6.QtGui import QCursor, QPixmap, QPainter, QPen, QColor, QPainterPath
from PySide6.QtWidgets import QLineEdit, QFileDialog
from editor.common.icon_cache import getThemePixmap

class TextLineEdit(QLineEdit):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.returnPressed.connect(self.clearFocus)

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.clear()
			self.clearFocus()
		else:
			super().keyPressEvent(evt)


class IntLineEdit(QLineEdit):
	pass


class FloatLineEdit(QLineEdit):
	pass


class SearchLineEdit(QLineEdit):
	@Property(QPixmap)
	def searchIcon(self):
		return self._pixmapSearch
	@searchIcon.setter
	def searchIcon(self, value):
		self._pixmapSearch = value

	@Property(QColor)
	def closeButtonLineColor(self):
		return self._penCloseButton.color()
	@closeButtonLineColor.setter
	def closeButtonLineColor(self, value):
		self._penCloseButton.setColor(value)
	@Property(int)
	def closeButtonLineWidth(self):
		return self._penCloseButton.width()
	@closeButtonLineWidth.setter
	def closeButtonLineWidth(self, value):
		self._penCloseButton.setWidth(value)

	def __init__(self, parent = None):
		super().__init__(parent)

		self._pixmapSearch = getThemePixmap('search.png')
		# self._pixmapClear  = getThemePixmap('close.png')
		self._penCloseButton = QPen(QColor('#ccc'), 1.5)

		self.setMouseTracking(True)
		self.textChanged.connect(self.onTextChange)
		self.returnPressed.connect(self.clearFocus)

		self._clearBtnVisible = False
		self._clearBtnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()

		self.setStyleSheet(f"""
			SearchLineEdit {{
				padding-right: {h-2}px;
				padding-left: {h-2}px;
			}}
		""")
		
		self._searchRect = QRect(0, 0, h, h)
		self._searchRect.adjust(2, 2, -2, -2)
		self._closeRect = QRect(w - h, 0, h, h)
		self._closeRect.adjust(2, 2, -2, -2)

	def onTextChange(self, text):
		showClearBtn = bool(text)
		if self._clearBtnVisible != showClearBtn:
			self._clearBtnVisible = showClearBtn
			self.update()

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.clear()
			self.clearFocus()
		else:
			super().keyPressEvent(evt)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		if not self._clearBtnVisible: return
		hover = self._closeRect.contains(evt.pos())
		if hover == self._clearBtnHovered: return
		if hover:
			self.setCursor(Qt.ArrowCursor)
		else:
			self.setCursor(Qt.IBeamCursor)
		self._clearBtnHovered = hover

	def mousePressEvent(self, evt):
		if self._clearBtnHovered:
			self.clear()
			self.setCursor(Qt.IBeamCursor)
			self._clearBtnHovered = False
		else:
			super().mousePressEvent(evt)

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		if self._clearBtnHovered:
			self._btnHovered = False
			self.setCursor(Qt.IBeamCursor)
			self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.drawPixmap(self._searchRect, self._pixmapSearch)
		if self._clearBtnVisible:
			# painter.drawPixmap(self._closeRect, self._pixmapClear)
			painter.setPen(self._penCloseButton)
			rect = self._closeRect.adjusted(4, 4, -4, -4)
			painter.drawLine(rect.topLeft(), rect.bottomRight())
			painter.drawLine(rect.topRight(), rect.bottomLeft())


class PlaceholderLineEdit(QLineEdit):
	def __init__(self, placeholder = None, parent = None):
		super().__init__(parent)
		self.prevTextIsEmpty = True
		self.setPlaceholderText(placeholder)
		self.textChanged.connect(self.onTextChanged)

	def onTextChanged(self, text):
		empty = not bool(text)
		if empty == self.prevTextIsEmpty: return
		self.prevTextIsEmpty = empty
		self.style().polish(self)


class PathLineEdit(QLineEdit):
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
	def buttonRadius(self):
		return self._btnRadius
	@buttonRadius.setter
	def buttonRadius(self, value):
		self._btnRadius = value

	def __init__(self, folderPath, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('folder_close.png')
		self._btnRadius = 2
		
		self._btnHovered = False

		self.setMouseTracking(True)
		self.returnPressed.connect(self.clearFocus)
		self.folderPath = folderPath

	def onButtonClick(self):
		base = os.environ[ 'DEAR_BASE_PATH' ]
		# curr = os.path.join(base, self.text())
		# root = curr if os.path.exists(curr) else base
		root = base

		if self.folderPath:
			path = QFileDialog.getExistingDirectory(self, 'Select Folder', root)
			if not path: return
			self.setText(os.path.relpath(path, base))

		else:
			# filters = 'All Files (*);;Text Files (*.txt)'
			# selectedFilter = 'Text Files (*.txt)'
			base = os.environ[ 'DEAR_BASE_PATH' ]
			path, _ = QFileDialog.getOpenFileName(self, 'Select File', root)
			if not path: return
			self.setText(os.path.relpath(path, base))

	def resizeEvent(self, event):
		super().resizeEvent(event)
		w, h = self.width(), self.height()
		self._btnRect = QRect(w - h, 0, h, h)
		self.setStyleSheet(f'PathLineEdit{{ padding-right: {h}px; }}')

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.clear()
			self.clearFocus()
		else:
			super().keyPressEvent(evt)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		hover = self._btnRect.contains(evt.pos())
		if hover == self._btnHovered: return
		if hover:
			self.setCursor(Qt.ArrowCursor)
		else:
			self.setCursor(Qt.IBeamCursor)
		self._btnHovered = hover
		self.update()

	def mousePressEvent(self, evt):
		if self._btnHovered:
			self.onButtonClick()
		else:
			super().mousePressEvent(evt)

	def mouseDoubleClickEvent(self, evt):
		if self._btnHovered:
			self.mousePressEvent(evt)
		else:
			super().mouseDoubleClickEvent(evt)

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		if self._btnHovered:
			self._btnHovered = False
			self.setCursor(Qt.IBeamCursor)
			self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		# painter.setRenderHint(QPainter.SmoothPixmapTransform)
		path = QPainterPath()
		radius = max(self._btnRadius - 1, 0)
		path.addRoundedRect(self.rect().adjusted(1, 1, -1, -1), radius, radius)
		painter.setClipPath(path)
		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(3, 3, -3, -3), self._pixmapBtnIcon)

