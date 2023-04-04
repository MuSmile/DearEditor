import os, platform
from PySide6.QtCore import Qt, QRect, Property, Signal, QEvent
from PySide6.QtGui import QCursor, QPixmap, QPainter, QPen, QColor, QPainterPath
from PySide6.QtWidgets import QLineEdit, QFileDialog, QFrame, QStyleOptionFrame, QStyle
from editor.common.icon_cache import getThemePixmap
from editor.common.util import toInt, toFloat, formatNumber
from editor.common.math import sign

class LineEdit(QLineEdit):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.returnPressed.connect(self.clearFocus)

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape: return self.clearFocus()
		super().keyPressEvent(evt)

	def eventFilter(self, obj, evt):
		"""For listening shortcut on MacOS popup...
		"""
		if evt.type() == QEvent.ShortcutOverride:
			self.event(evt)
			return True
		return False


class IntLineEdit(LineEdit):
	valueChanged = Signal(int)

	def __init__(self, value = 0, step = 1, parent = None):
		super().__init__(parent)
		self.step = step
		self.value = value
		self.setText(str(value))
		self.textEdited.connect(self.onTextEdited)

	def onTextEdited(self, text):
		if text[-1] == '.': text = text[:-1]
		value = toInt(text)
		if self.value == value: return
		self.value = value
		self.valueChanged.emit(value)
		
	def setValue(self, value):
		if self.value == value: return
		self.value = value
		self.setText(str(value))
		self.valueChanged.emit(value)

	def checkValue(self):
		text = self.text()
		if text[-1] == '.': text = text[:-1]
		value = str(toInt(text))
		if text != value: self.setText(value)

	def focusOutEvent(self, evt):
		super().focusOutEvent(evt)
		self.checkValue()

	def wheelEvent(self, evt):
		if not self.hasFocus(): return evt.ignore()
		angleDelta = evt.angleDelta()
		shiftPressed = evt.modifiers() & Qt.ShiftModifier
		if shiftPressed:
			dy = sign(angleDelta.x()) if platform.system() == 'Darwin' else sign(angleDelta.y())
			self.setValue(self.value + dy * self.step * 10)
		else:
			dy = sign(angleDelta.y())
			self.setValue(self.value + dy * self.step)
			

class FloatLineEdit(LineEdit):
	valueChanged = Signal(float)

	def __init__(self, value = 0, step = 0.01, parent = None):
		super().__init__(parent)
		self.step = step
		self.value = value
		self.sigFigures = 6
		self.setText(str(value))
		self.textEdited.connect(self.onTextEdited)

	def onTextEdited(self, text):
		raw = round(toFloat(text), self.sigFigures)
		value = formatNumber(raw)
		if self.value == value: return
		self.value = value
		self.valueChanged.emit(value)
		
	def setValue(self, value):
		raw = round(value, self.sigFigures)
		value = formatNumber(raw)
		if self.value == value: return
		self.value = value
		self.setText(str(value))
		self.valueChanged.emit(value)

	def checkValue(self):
		text = self.text()
		raw = round(toFloat(text), self.sigFigures)
		dstText = str(formatNumber(raw))
		if text != dstText: self.setText(dstText)

	def focusOutEvent(self, evt):
		super().focusOutEvent(evt)
		self.checkValue()

	def wheelEvent(self, evt):
		if not self.hasFocus(): return evt.ignore()
		angleDelta = evt.angleDelta()
		shiftPressed = evt.modifiers() & Qt.ShiftModifier
		if shiftPressed:
			dy = sign(angleDelta.x()) if platform.system() == 'Darwin' else sign(angleDelta.y())
			self.setValue(self.value + dy * self.step * 10)
		else:
			dy = sign(angleDelta.y())
			self.setValue(self.value + dy * self.step)


class SearchLineEdit(LineEdit):
	@Property(QPixmap)
	def searchIcon(self):
		return self._pixmapSearch
	@searchIcon.setter
	def searchIcon(self, value):
		self._pixmapSearch = value

	@Property(QPixmap)
	def clearIcon(self):
		return self._pixmapClear
	@clearIcon.setter
	def clearIcon(self, value):
		self._pixmapClear = value

	def __init__(self, parent = None):
		super().__init__(parent)

		self._pixmapSearch = getThemePixmap('search.png')
		self._pixmapClear  = getThemePixmap('close.png')

		self.setMouseTracking(True)
		self.textChanged.connect(self.onTextChange)

		self._clearBtnVisible = False
		self._clearBtnHovered = False

	def resizeEvent(self, event):
		super().resizeEvent(event)
		rect = self.contentsRect()
		x, y = rect.x(), rect.y()
		r, h = rect.right(), rect.height()

		self.setStyleSheet(f"""
			SearchLineEdit {{
				padding-right: {h-2}px;
				padding-left: {h-2}px;
			}}
		""")

		self._searchRect = QRect(x, y, h, h)
		self._searchRect.adjust(2, 2, -2, -2)
		self._closeRect = QRect(r - h, y, h, h)
		self._closeRect.adjust(2, 2, -2, -2)

	def onTextChange(self, text):
		showClearBtn = bool(text)
		if self._clearBtnVisible != showClearBtn:
			self._clearBtnVisible = showClearBtn
			self.update()

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape: self.clear()
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
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.drawPixmap(self._searchRect, self._pixmapSearch)
		if self._clearBtnVisible:
			painter.drawPixmap(self._closeRect, self._pixmapClear)


class PlaceholderLineEdit(LineEdit):
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


class PathLineEdit(LineEdit):
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

	def __init__(self, folderPath, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('folder_close.png')
		self._borderRadius = 2
		self._marginLeft = 0
		self._marginRight = 0
		
		self._btnHovered = False

		self.setMouseTracking(True)
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
		self._btnRect = QRect(w - h - self._marginRight, 0, h, h)
		self.setStyleSheet(f'PathLineEdit{{ padding-right: {h}px; }}')

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
		rect = self.rect().adjusted(self._marginLeft, 0, -self._marginRight, 0)
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(2, 2, -2, -2), self._pixmapBtnIcon)

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		painter.setClipping(False)
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
