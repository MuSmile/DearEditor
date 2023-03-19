import os
from PySide6.QtCore import Qt, QRect, Property, Signal
from PySide6.QtGui import QCursor, QPixmap, QPainter, QPen, QColor, QPainterPath
from PySide6.QtWidgets import QLineEdit, QFileDialog, QStyle, QStyleOption
from editor.common.icon_cache import getThemePixmap
from editor.common.util import toInt, toFloat
from editor.common.math import sign

class LineEdit(QLineEdit):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.returnPressed.connect(self.clearFocus)

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape: self.clearFocus()
		super().keyPressEvent(evt)


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
		if not self.hasFocus(): return
		angleDelta = evt.angleDelta()
		shiftPressed = evt.modifiers() & Qt.ShiftModifier
		delta = sign(angleDelta.x()) * 10 if shiftPressed else sign(angleDelta.y())
		self.setValue(self.value + delta * self.step)


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
		value = round(toFloat(text), self.sigFigures)
		if self.value == value: return
		self.value = value
		self.valueChanged.emit(value)
		
	def setValue(self, value):
		value = round(value, self.sigFigures)
		if self.value == value: return
		self.value = value
		self.setText(str(value))
		self.valueChanged.emit(value)

	def checkValue(self):
		text = self.text()
		value = str(round(toFloat(text), self.sigFigures))
		if text != value: self.setText(value)

	def focusOutEvent(self, evt):
		super().focusOutEvent(evt)
		self.checkValue()

	def wheelEvent(self, evt):
		if not self.hasFocus(): return
		angleDelta = evt.angleDelta()
		shiftPressed = evt.modifiers() & Qt.ShiftModifier
		delta = sign(angleDelta.x()) * 10 if shiftPressed else sign(angleDelta.y())
		self.setValue(self.value + delta * self.step)


class SearchLineEdit(LineEdit):
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
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.drawPixmap(self._searchRect, self._pixmapSearch)
		if self._clearBtnVisible:
			# painter.drawPixmap(self._closeRect, self._pixmapClear)
			painter.setPen(self._penCloseButton)
			rect = self._closeRect.adjusted(4, 4, -4, -4)
			painter.drawLine(rect.topLeft(), rect.bottomRight())
			painter.drawLine(rect.topRight(), rect.bottomLeft())


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

	def __init__(self, folderPath, parent = None):
		super().__init__(parent)

		self._btnColor = QColor('#444')
		self._btnColorHovered = QColor('#666')
		self._pixmapBtnIcon = getThemePixmap('folder_close.png')

		self._borderColor = QColor('#222')
		self._borderColorHovered = QColor('#777')
		self._borderColorFocused = QColor('#5ae')
		self._borderColorReadonly = QColor('gray')
		self._borderRadius = 2
		self._penBorder = QPen(self._borderColor, 2)
		
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
		self._btnRect = QRect(w - h, 0, h, h)
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
		rect = self.rect()
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		painter.fillRect(self._btnRect, self._btnColorHovered if self._btnHovered else self._btnColor)
		painter.drawPixmap(self._btnRect.adjusted(3, 3, -3, -3), self._pixmapBtnIcon)

		option = QStyleOption()
		option.initFrom(self)
		if option.state & QStyle.State_HasFocus:
			self._penBorder.setColor(self._borderColorFocused)
		elif option.state & QStyle.State_MouseOver:
			self._penBorder.setColor(self._borderColorHovered)
		else:
			self._penBorder.setColor(self._borderColor)

		painter.setPen(self._penBorder)
		painter.drawRoundedRect(rect, self._borderRadius, self._borderRadius)
