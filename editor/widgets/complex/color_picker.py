from PySide6.QtCore import Qt, Signal, QRect, QRectF, QRegularExpression
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QMenu, QHBoxLayout, QVBoxLayout, QApplication
from PySide6.QtGui import QColor, QPainter, QPainterPath, QLinearGradient, QConicalGradient, QRegularExpressionValidator, QPixmap, QImage, QCursor, QPen
from editor.common.math import clamp, locAt, vecAngle, lerpI, getDir
from editor.common.util import getIde, requestTransparentBgBrush, toInt, toFloat, isParentOfWidget
from editor.common.icon_cache import getThemePixmap


#####################  INTERNAL  #####################
_ColorSpaceLabels = ['RGB 0-255', 'RGB 0-1.0', 'HSV      ']
_ColorSpaceRgb, _ColorSpaceRgbF, _ColorSpaceHsv = range(3)

class _ColorRing(QWidget):
	def color(self): return self.parent().currentColor
	def setColor(self, h, s, v, a):
		parent = self.parent()
		parent.currentColor.setHsvF(h, s, v, a)
		parent.updateCurrentColor('ring')

	def __init__(self, parent):
		super().__init__(parent)
		size = parent.width()
		self.ringWidth = 24
		self.ringRadius = 96
		self.setFixedSize(size, size)
		self.buildColorRing()
		# self.updateColorRectImage()
		self.mouseTarget = None
		self.overridePaintFunc = None
		self.cachedHue = None
		parent.colorChanged.connect(self.update)

	def buildColorRing(self):
		path = QPainterPath()
		rw = self.ringWidth
		x = self.width() / 2 - self.ringRadius - rw / 2
		w = self.ringRadius * 2 + rw
		rect = QRectF(x, x, w, w)
		path.addEllipse(rect)
		path.addEllipse(rect.adjusted(rw, rw, -rw, -rw))

		gradient = QConicalGradient(rect.center(), 0)
		gradient.setColorAt(0,   QColor(255,   0,   0))
		gradient.setColorAt(1/6, QColor(255, 255,   0))
		gradient.setColorAt(2/6, QColor(  0, 255,   0))
		gradient.setColorAt(3/6, QColor(  0, 255, 255))
		gradient.setColorAt(4/6, QColor(  0,   0, 255))
		gradient.setColorAt(5/6, QColor(255,   0, 255))
		gradient.setColorAt(1,   QColor(255,   0,   0))

		self.ringPath = path
		self.ringGradient = gradient

		offset = 57
		self.colorRect = rect.toRect().adjusted(offset, offset, -offset, -offset)
		self.colorRectImage = QImage(self.colorRect.size(), QImage.Format_RGB888)

	def updateColorRectImage(self, hue):
		w, h = self.colorRect.width(), self.colorRect.height()
		# hue = clamp(self.color().hsvHueF(), 0, 1)
		for x in range(h):
			saturation = x / (h-1)
			for y in range(w):
				value = 1 - y / (w-1)
				self.colorRectImage.setPixelColor(x, y, QColor.fromHsvF(hue, saturation, value))

	def paintEvent(self, evt):
		hue = clamp(self.color().hsvHueF(), 0, 1)
		if self.cachedHue != hue or self.cachedHue == None:
			self.updateColorRectImage(hue)

		painter = QPainter(self)
		if self.overridePaintFunc: return self.overridePaintFunc(painter)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.fillPath(self.ringPath, self.ringGradient)
		painter.drawImage(self.colorRect, self.colorRectImage)

		# draw ring pos
		angle = self.color().hue()
		dx, dy = vecAngle(angle, self.ringRadius)
		center = self.width() / 2
		x, y = round(center + dx), round(center - dy)
		r = self.ringWidth // 2 - 2
		painter.setPen(QPen(Qt.white, 2))
		painter.drawEllipse(x - r, y - r, r*2, r*2)

		# draw rect pos
		x = self.color().saturationF()
		y = self.color().valueF()
		x1, x2 = self.colorRect.left(), self.colorRect.right()
		y1, y2 = self.colorRect.top(), self.colorRect.bottom()
		x, y = lerpI(x1, x2, x), lerpI(y2, y1, y)
		r = 6
		R, G, B, A = self.color().getRgbF()
		brightness = 0.2126*R + 0.7152*G + 0.0722*B
		if brightness < 0.5:
			painter.setPen(QPen(Qt.white, 1.2))
		else:
			painter.setPen(QPen(Qt.black, 1.2))
		painter.drawEllipse(x - r, y - r, r*2, r*2)

	def checkInsideRing(self, pos):
		center = self.width() / 2
		dx, dy = pos.x() - center, pos.y() - center
		dist2 = dx * dx + dy * dy
		rin = self.ringRadius - self.ringWidth / 2
		rout = self.ringRadius + self.ringWidth / 2
		return rin * rin <= dist2 <= rout * rout

	def mousePressEvent(self, evt):
		pos = evt.pos()
		if self.colorRect.contains(pos):
			x1, x2 = self.colorRect.left(), self.colorRect.right()
			y1, y2 = self.colorRect.top(), self.colorRect.bottom()
			x, y = locAt(x1, x2, pos.x()), locAt(y2, y1, pos.y())
			h, s, v, a = self.color().getHsvF()
			self.setColor(h, x, y, a)
			self.mouseTarget = 'rect'

		elif self.checkInsideRing(pos):
			center = self.width() / 2
			dx, dy = pos.x() - center, pos.y() - center
			angle = getDir(dx, -dy) % 360
			h, s, v, a = self.color().getHsvF()
			self.setColor(angle/360, s, v, a)
			self.mouseTarget = 'ring'
			# self.updateColorRectImage()

		else:
			self.mouseTarget = None

	def mouseMoveEvent(self, evt):
		pos = evt.pos()
		if self.mouseTarget == 'rect':
			x1, x2 = self.colorRect.left(), self.colorRect.right()
			y1, y2 = self.colorRect.top(), self.colorRect.bottom()
			x, y = locAt(x1, x2, pos.x()), locAt(y2, y1, pos.y())
			h, s, v, a = self.color().getHsvF()
			self.setColor(clamp(h, 0, 1), clamp(x, 0, 1), clamp(y, 0, 1), a)

		elif self.mouseTarget == 'ring':
			center = self.width() / 2
			dx, dy = pos.x() - center, pos.y() - center
			angle = getDir(dx, -dy) % 360
			h, s, v, a = self.color().getHsvF()
			self.setColor(angle/360, s, v, a)
			# self.updateColorRectImage()

class _ColorPickerBtn(QWidget):
	clicked = Signal()

	def __init__(self, parent):
		super().__init__(parent)
		self.setFixedSize(20, 20)
		self.setToolTip('Pick a color from the screen')

	def mousePressEvent(self, evt):
		if evt.button() == Qt.LeftButton:
			self.clicked.emit()

	def paintEvent(self, evt):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.drawPixmap(self.rect(), getThemePixmap('color_picker.png'))

class _ColorPreview(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.setFixedSize(76, 24)
		self.setMouseTracking(True)
		self.tooltipL = 'The original color. Click to reset to this.'
		self.tooltipR = 'The new color.'
		self.useTooltipL = True
		self.setToolTip(self.tooltipL)
		parent.colorChanged.connect(self.update)

	def mousePressEvent(self, evt):
		if evt.button() == Qt.LeftButton:
			x = evt.x()
			if x < self.width() // 2:
				self.parent().revertColor()

	def mouseMoveEvent(self, evt):
		x = evt.x()
		inLeft = x < self.width() // 2
		if inLeft and not self.useTooltipL:
			self.useTooltipL = True
			self.setToolTip(self.tooltipL)
		elif not inLeft and self.useTooltipL:
			self.useTooltipL = False
			self.setToolTip(self.tooltipR)

	def paintEvent(self, evt):
		painter = QPainter(self)
		# painter.setRenderHint(QPainter.Antialiasing)
		path = QPainterPath()
		w, h = self.width(), self.height()
		path.addRoundedRect(0, 0, w, h, 2, 2)
		painter.setClipPath(path)

		wHalf = w // 2
		parent = self.parent()
		brush = requestTransparentBgBrush()
		# painter.setPen(Qt.transparent)
		# painter.setBrush(brush)
		# painter.drawRoundedRect(0, 0, w, h, 5, 5)
		painter.fillRect(0, 0, w, h, brush)
		painter.fillRect(0, 0, wHalf, h, parent.initColor)
		painter.fillRect(wHalf, 0, wHalf, h, parent.currentColor)

class _ColorSpaceDropDown(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)
		self.setFocusPolicy(Qt.NoFocus)
		self.setText(_ColorSpaceLabels[ColorPicker.ColorSpace])
		self.pressed.connect(self.showMenu)
		self.setFixedSize(88, 24)
		self.initMenu()

	def initMenu(self):
		actions = []
		menu = QMenu(self)
		# menu.setAttribute(Qt.WA_TranslucentBackground)
		# menu.setWindowFlag(Qt.FramelessWindowHint, True)
		for label in _ColorSpaceLabels: actions.append(menu.addAction(label))
		for act in actions: act.setCheckable(True)
		actions[ColorPicker.ColorSpace].setChecked(True)
		menu.triggered.connect(self.onActionTrigger)
		self.setMenu(menu)

	def onActionTrigger(self, action):
		actions = self.menu().actions()
		self.setText(action.text())
		for act in actions: act.setChecked(act == action)
		self.parent().updateColorSpace(actions.index(action))

class _ColorCptSlot(QWidget):
	def __init__(self, parent, isAlpha = False):
		super().__init__(parent)
		self.value = 0
		self.isAlpha = isAlpha
		self.handleWidth = 4

	def updateValue(self, value, updateColor = False):
		self.update()
		if value == self.value: return
		self.value = value
		if updateColor:
			cpt = self.parent().cpt
			editor = self.parent().parent()
			if cpt == _ColorComponentEdit.CptA:
				r, g, b, a = editor.currentColor.getRgbF()
				editor.currentColor.setRgbF(r, g, b, value)
			elif cpt == _ColorComponentEdit.CptR:
				r, g, b, a = editor.currentColor.getRgbF()
				editor.currentColor.setRgbF(value, g, b, a)
			elif cpt == _ColorComponentEdit.CptG:
				r, g, b, a = editor.currentColor.getRgbF()
				editor.currentColor.setRgbF(r, value, b, a)
			elif cpt == _ColorComponentEdit.CptB:
				r, g, b, a = editor.currentColor.getRgbF()
				editor.currentColor.setRgbF(r, g, value, a)
			elif cpt == _ColorComponentEdit.CptH:
				h, s, v, a = editor.currentColor.getHsvF()
				editor.currentColor.setHsvF(value, s, v, a)
			elif cpt == _ColorComponentEdit.CptS:
				h, s, v, a = editor.currentColor.getHsvF()
				editor.currentColor.setHsvF(h, value, v, a)
			elif cpt == _ColorComponentEdit.CptV:
				h, s, v, a = editor.currentColor.getHsvF()
				editor.currentColor.setHsvF(h, s, value, a)
			editor.updateCurrentColor(f'slot{cpt}')

	def buildGradient(self):
		gradient = QLinearGradient()
		cpt = self.parent().cpt
		color = self.parent().parent().currentColor
		r, g, b, a = color.getRgbF()
		if cpt == _ColorComponentEdit.CptA:
			gradient.setColorAt(0, QColor.fromRgbF(r, g, b, 0))
			gradient.setColorAt(1, QColor.fromRgbF(r, g, b, 1))
		elif cpt == _ColorComponentEdit.CptR:
			gradient.setColorAt(0, QColor.fromRgbF(0, g, b))
			gradient.setColorAt(1, QColor.fromRgbF(1, g, b))
		elif cpt == _ColorComponentEdit.CptG:
			gradient.setColorAt(0, QColor.fromRgbF(r, 0, b))
			gradient.setColorAt(1, QColor.fromRgbF(r, 1, b))
		elif cpt == _ColorComponentEdit.CptB:
			gradient.setColorAt(0, QColor.fromRgbF(r, g, 0))
			gradient.setColorAt(1, QColor.fromRgbF(r, g, 1))
		elif cpt == _ColorComponentEdit.CptH:
			gradient.setColorAt(0,   QColor.fromHsvF(0,   1, 1))
			gradient.setColorAt(1/6, QColor.fromHsvF(1/6, 1, 1))
			gradient.setColorAt(2/6, QColor.fromHsvF(2/6, 1, 1))
			gradient.setColorAt(3/6, QColor.fromHsvF(3/6, 1, 1))
			gradient.setColorAt(4/6, QColor.fromHsvF(4/6, 1, 1))
			gradient.setColorAt(5/6, QColor.fromHsvF(5/6, 1, 1))
			gradient.setColorAt(1,   QColor.fromHsvF(1,   1, 1))
		elif cpt == _ColorComponentEdit.CptS:
			h, s, v, a = color.getHsvF()
			gradient.setColorAt(0, QColor.fromHsvF(h, 0, v))
			gradient.setColorAt(1, QColor.fromHsvF(h, 1, v))
		elif cpt == _ColorComponentEdit.CptV:
			h, s, v, a = color.getHsvF()
			gradient.setColorAt(0, QColor.fromHsvF(h, s, 0))
			gradient.setColorAt(1, QColor.fromHsvF(h, s, 1))
		return gradient

	def paintEvent(self, evt):
		rect = self.rect()
		w, h = rect.width(), rect.height()
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(QColor('#222'))
		if self.isAlpha:
			brush = requestTransparentBgBrush()
			painter.setBrush(brush)
			painter.drawRect(rect)

		hw = self.handleWidth
		gradient = self.buildGradient()
		gradient.setStart(hw/2, 0)
		gradient.setFinalStop(w - hw/2, 0)
		painter.setBrush(gradient)
		painter.drawRect(rect)

		painter.setPen(QColor('#aaa'))
		painter.setBrush(QColor('#ccc'))
		x = round((w - hw) * self.value)
		painter.drawRect(x, 0, hw, h)

	def mousePressEvent(self, evt):
		x = evt.x()
		hhw = self.handleWidth / 2
		value = locAt(hhw, self.width() - hhw, x)
		self.updateValue(clamp(value, 0, 1), True)
	def mouseMoveEvent(self, evt):
		x = evt.x()
		hhw = self.handleWidth / 2
		value = locAt(hhw, self.width() - hhw, x)
		self.updateValue(clamp(value, 0, 1), True)

class _ColorCptLineEdit(QLineEdit):
	def __init__(self, parent):
		super().__init__(parent)
		self.setFocusPolicy(Qt.StrongFocus)
		self.value = None
		self.editingFinished.connect(self.onEditingFinish)
		self.textChanged.connect(self.onTextChange)
		self.ignoreUpdate = True
		# self.setStyleSheet('padding-right: -10px;')

	def parseText(self, text):
		space = ColorPicker.ColorSpace
		if space == _ColorSpaceRgb:
			return clamp(toInt(text), 0, 255)
		elif space == _ColorSpaceRgbF:
			return clamp(toFloat(text), 0.0, 1.0)
		else:
			hue = self.parent().cpt == _ColorComponentEdit.CptH
			return clamp(toInt(text), 0, hue and 360 or 100)

	def onTextChange(self, text):
		value = self.parseText(text)
		if self.value == value: return
		self.value = value
		if self.ignoreUpdate: return
		cpt = self.parent().cpt
		space = ColorPicker.ColorSpace
		editor = self.parent().parent()
		if space == _ColorSpaceRgb:
			r, g, b, a = editor.currentColor.getRgb()
			if cpt == _ColorComponentEdit.CptR:
				editor.currentColor.setRgb(value, g, b, a)
			elif cpt == _ColorComponentEdit.CptG:
				editor.currentColor.setRgb(r, value, b, a)
			elif cpt == _ColorComponentEdit.CptB:
				editor.currentColor.setRgb(r, g, value, a)
			elif cpt == _ColorComponentEdit.CptA:
				editor.currentColor.setRgb(r, g, b, value)

		elif space == _ColorSpaceRgbF:
			r, g, b, a = editor.currentColor.getRgbF()
			if cpt == _ColorComponentEdit.CptR:
				editor.currentColor.setRgbF(value, g, b, a)
			elif cpt == _ColorComponentEdit.CptG:
				editor.currentColor.setRgbF(r, value, b, a)
			elif cpt == _ColorComponentEdit.CptB:
				editor.currentColor.setRgbF(r, g, value, a)
			elif cpt == _ColorComponentEdit.CptA:
				editor.currentColor.setRgbF(r, g, b, value)

		else:
			h, s, v, a = editor.currentColor.getHsv()
			if cpt == _ColorComponentEdit.CptH:
				editor.currentColor.setHsv(value, s, v, a)
			elif cpt == _ColorComponentEdit.CptS:
				editor.currentColor.setHsv(h, value, v, a)
			elif cpt == _ColorComponentEdit.CptV:
				editor.currentColor.setHsv(h, s, value, a)
			elif cpt == _ColorComponentEdit.CptA:
				editor.currentColor.setHsv(h, s, v, value)

		editor.updateCurrentColor(f'edit{cpt}')

	def onEditingFinish(self):
		self.ignoreUpdate = True
		self.parent().updateLineEdit()
		self.setText(str(self.value))
		self.home(False)
		self.clearFocus()

	def mouseDoubleClickEvent(self, evt):
		if evt.button() == Qt.LeftButton: return self.selectAll()
		super().mouseDoubleClickEvent(evt)

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.ignoreUpdate = True
			self.setText(self.originText)
			self.home(False)
			self.clearFocus()
		else:
			super().keyPressEvent(evt)

	def focusInEvent(self, evt):
		super().focusInEvent(evt)
		self.originText = self.text()
		self.ignoreUpdate = False

	def focusOutEvent(self, evt):
		super().focusOutEvent(evt)
		self.ignoreUpdate = True

	def wheelEvent(self, evt):
		if not self.hasFocus(): return
		dy = sign(evt.angleDelta().y())
		self.updateWithDelta(dy)
		# self.home(False)

	def updateWithDelta(self, deltaDir):
		space = ColorPicker.ColorSpace
		if space == _ColorSpaceRgb:
			value = clamp(self.value + deltaDir * 5, 0, 255)
			self.setText(str(value))
		elif space == _ColorSpaceRgbF:
			value = clamp(self.value + deltaDir * 0.05, 0.0, 1.0)
			value = round(value * 10000) / 10000
			self.setText(str(value))
		else:
			if self.parent().cpt == _ColorComponentEdit.CptH:
				value = clamp(self.value + deltaDir * 5, 0, 360)
				self.setText(str(value))
			else:
				value = clamp(self.value + deltaDir * 5, 0, 100)
				self.setText(str(value))

class _ColorCptLabel(QLabel):
	moveTriggered = Signal(int)

	def __init__(self, parent):
		super().__init__(parent)
		self.setStyleSheet('padding-bottom: 2px; color: #ccc;')
		self.setCursor(QCursor(getThemePixmap('field_cursor.png'), 8, 2))
		self.mouseDownPos = None
		self.prevMousePos = None
		# self.moveTriggered.connect(lambda dm: print(dm))

	def mousePressEvent(self, evt):
		if evt.button() != Qt.LeftButton: return
		self.mouseDownPos = evt.pos()
		self.prevMousePos = None

	def mouseMoveEvent(self, evt):
		# if not self.mouseDownPos: return
		pos = evt.pos()
		if self.prevMousePos:
			dx = pos.x() - self.prevMousePos.x()
			if dx > 3:
				self.prevMousePos = pos
				self.moveTriggered.emit(1)
			elif dx < -3:
				self.prevMousePos = pos
				self.moveTriggered.emit(-1)
		else:
			dx = pos.x() - self.mouseDownPos.x()
			if dx > 10:
				self.prevMousePos = pos
				self.moveTriggered.emit(1)
			elif dx < -10:
				self.prevMousePos = pos
				self.moveTriggered.emit(-1)

class _ColorComponentEdit(QWidget):
	CptA, CptR, CptG, CptB, CptH, CptS, CptV = range(7)
	CptLabels = ['A', 'R', 'G', 'B', 'H', 'S', 'V']

	def componentValue(self):
		parent = self.parent()
		color = parent.currentColor
		space = parent.ColorSpace
		if self.cpt == self.CptA:
			if   space == _ColorSpaceRgbF: return color.alphaF()
			elif space == _ColorSpaceHsv: return round(color.alphaF() * 100)
			else: return color.alpha()
		elif self.cpt == self.CptR:
			if space == _ColorSpaceRgbF: return color.redF()
			else: return color.red()
		elif self.cpt == self.CptG:
			if space == _ColorSpaceRgbF: return color.greenF()
			else: return color.green()
		elif self.cpt == self.CptB:
			if space == _ColorSpaceRgbF: return color.blueF()
			else: return color.blue()
		elif self.cpt == self.CptH:
			return max(color.hue(), 0)
		elif self.cpt == self.CptS:
			return round(color.saturationF() * 100)
		elif self.cpt == self.CptV:
			return round(color.valueF() * 100)

	def componentValueF(self):
		color = self.parent().currentColor
		if self.cpt == self.CptA:
			return color.alphaF()
		elif self.cpt == self.CptR:
			return color.redF()
		elif self.cpt == self.CptG:
			return color.greenF()
		elif self.cpt == self.CptB:
			return color.blueF()
		elif self.cpt == self.CptH:
			return color.hueF()
		elif self.cpt == self.CptS:
			return color.saturationF()
		elif self.cpt == self.CptV:
			return color.valueF()

	def __init__(self, parent, cpt):
		super().__init__(parent)
		layout = QHBoxLayout(self)
		layout.setContentsMargins(8, 0, 10, 8)
		layout.setSpacing(6)

		label = _ColorCptLabel(self)
		label.setFixedWidth(13)
		layout.addWidget(label)

		slot = _ColorCptSlot(self, cpt == self.CptA)
		slot.setFixedHeight(18)
		layout.addWidget(slot)
		layout.setStretch(1, 1)

		lineEdit = _ColorCptLineEdit(self)
		lineEdit.setFixedSize(43, 18)
		layout.addWidget(lineEdit)

		self.label = label
		self.slot = slot
		self.lineEdit = lineEdit
		self.cpt = None
		self.updateComponent(cpt)
		# slot.updateValue(self.componentValueF())
		def onLabelMove(delta):
			lineEdit.ignoreUpdate = False
			lineEdit.updateWithDelta(delta)
			lineEdit.ignoreUpdate = True
		label.moveTriggered.connect(onLabelMove)
		parent.colorChanged.connect(self.onCurrentColorChange)

	def updateLineEdit(self):
		space = ColorPicker.ColorSpace
		if space == _ColorSpaceRgbF:
			value = round(self.componentValue() * 1000) / 1000
			self.lineEdit.setText(str(value))
		else:
			self.lineEdit.setText(str(self.componentValue()))

		self.lineEdit.home(False)

	def updateComponent(self, cpt):
		# if self.cpt == cpt: return
		self.cpt = cpt
		self.label.setText(self.CptLabels[cpt])
		self.slot.updateValue(self.componentValueF())
		self.updateLineEdit()

	def onCurrentColorChange(self, color, reason):
		if reason != f'slot{self.cpt}': self.slot.updateValue(self.componentValueF())
		if reason != f'edit{self.cpt}': self.updateLineEdit()

class _ColorHexEditValidator(QRegularExpressionValidator):
	def __init__(self, parent):
		super().__init__(QRegularExpression('[A-Fa-f0-9]{,6}'), parent)

	def validate(self, string, pos):
		state, text, pos = super().validate(string, pos)
		return state, text.upper(), pos

class _ColorHexEdit(QLineEdit):
	def __init__(self, parent):
		super().__init__(parent)
		self.setFocusPolicy(Qt.StrongFocus)
		self.setValidator(_ColorHexEditValidator(self))
		self.setStyleSheet('padding-left: 12px;')
		self.onCurrentColorChange(parent.currentColor, None)
		parent.colorChanged.connect(self.onCurrentColorChange)
		self.editingFinished.connect(self.onEditingFinish)
		self.textChanged.connect(self.onTextChange)
		self.ignoreUpdate = True
		self.value = None

	def parseText(self, text):
		length = len(text)
		if length == 6 or length == 3: return text
		return False

	def onTextChange(self, text):
		tlen = len(text)
		if tlen != 6 and tlen != 3: return
		if self.value == text: return
		self.value = text
		if self.ignoreUpdate: return
		parent = self.parent()
		parent.currentColor.setNamedColor('#' + text)
		parent.updateCurrentColor('hex')

	def onEditingFinish(self):
		self.ignoreUpdate = True
		self.setText(self.value)
		self.clearFocus()

	def onCurrentColorChange(self, color, reason):
		if reason == 'hex': return
		self.setText(color.name()[1:].upper())

	def mouseDoubleClickEvent(self, evt):
		if evt.button() == Qt.LeftButton: return self.selectAll()
		super().mouseDoubleClickEvent(evt)

	def keyPressEvent(self, evt):
		if evt.key() == Qt.Key_Escape:
			self.ignoreUpdate = True
			self.setText(self.originText)
			self.clearFocus()
		else:
			super().keyPressEvent(evt)

	def focusInEvent(self, evt):
		super().focusInEvent(evt)
		self.originText = self.text()
		self.ignoreUpdate = False

	def focusOutEvent(self, evt):
		super().focusOutEvent(evt)
		self.ignoreUpdate = True

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setPen(QColor('#bbb'))
		painter.setFont(self.font())
		painter.drawText(5, 14, '#')


#####################  PUBLIC  #####################
class ColorPicker(QWidget):
	colorChanged = Signal(QColor, str) # color: QColor, reason: str
	
	ColorSpace = _ColorSpaceRgb

	def __init__(self, initColor = None):
		ide = getIde()
		super().__init__(ide.activeWindow())
		ide.focusChanged.connect(self.onFocusChange)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		# self.setWindowFlags(Qt.Drawer | Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		self.setWindowTitle('Color Picker')
		self.setFocusPolicy(Qt.ClickFocus)
		self.setFocus()

		w, h = 234, 468
		self.setFixedSize(w, h)
		pos = QCursor.pos()
		screen = self.screen().geometry()
		pos.setX(clamp(pos.x(), screen.left(), screen.right() - w))
		pos.setY(clamp(pos.y() - 30, screen.top(), screen.bottom() - h))

		self.move(pos)
		self.initColor = QColor(initColor)
		self.currentColor = QColor(initColor)

		btn = _ColorPickerBtn(self)
		btn.clicked.connect(self.pickScreenshotColor)
		preview = _ColorPreview(self)
		ring = _ColorRing(self)
		space = _ColorSpaceDropDown(self)
		cpt1, cpt2, cpt3 = None, None, None
		if self.ColorSpace == _ColorSpaceHsv:
			cpt1 = _ColorComponentEdit(self, _ColorComponentEdit.CptH)
			cpt2 = _ColorComponentEdit(self, _ColorComponentEdit.CptS)
			cpt3 = _ColorComponentEdit(self, _ColorComponentEdit.CptV)
		else:
			cpt1 = _ColorComponentEdit(self, _ColorComponentEdit.CptR)
			cpt2 = _ColorComponentEdit(self, _ColorComponentEdit.CptG)
			cpt3 = _ColorComponentEdit(self, _ColorComponentEdit.CptB)
		cptA = _ColorComponentEdit(self, _ColorComponentEdit.CptA)

		layout = QVBoxLayout(self)
		layout.setAlignment(Qt.AlignTop)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		layoutH = QHBoxLayout()
		layoutH.setContentsMargins(10, 12, 10, 2)
		layoutH.setSpacing(0)
		layoutH.addWidget(btn)
		layoutH.addStretch()
		layoutH.addWidget(preview)
		layout.addLayout(layoutH)

		layout.addWidget(ring)

		layoutH = QHBoxLayout()
		layoutH.setContentsMargins(0, 5, 10, 0)
		layoutH.setSpacing(0)
		layoutH.addStretch()
		layoutH.addWidget(space)
		layout.addLayout(layoutH)

		layout.addSpacing(7)
		layout.addWidget(cpt1)
		layout.addWidget(cpt2)
		layout.addWidget(cpt3)
		layout.addWidget(cptA)

		hexLabel = QLabel('Hexadecimal', self)
		hexLabel.setStyleSheet('color: #ccc;')
		hexEdit = _ColorHexEdit(self)
		hexEdit.setFixedWidth(80)
		layoutH = QHBoxLayout()
		layoutH.setContentsMargins(11, 0, 10, 7)
		layoutH.setSpacing(0)
		layoutH.addWidget(hexLabel)
		layoutH.addStretch()
		layoutH.addWidget(hexEdit)
		layout.addLayout(layoutH)

		presetBtn = QPushButton('Color Presets Editor', self)
		presetBtn.setStyleSheet('QPushButton { margin: 0 10 0 10; height: 12px; }')
		presetBtn.setFocusPolicy(Qt.NoFocus)
		# presetBtn.clicked.connect(self.toggleColorPresetEditor)
		layout.addWidget(presetBtn)

		self.colorRing = ring
		self.colorCpt1 = cpt1
		self.colorCpt2 = cpt2
		self.colorCpt3 = cpt3
		self.colorCptA = cptA

		self.screenColorPickers = {}

	def paintEvent(self, evt):
		painter = QPainter(self)
		painter.fillRect(self.rect(), QColor('#444'))
		super().paintEvent(evt)

	def closeEvent(self, evt):
		super().closeEvent(evt)
		getIde().focusChanged.disconnect(self.onFocusChange)

	def onFocusChange(self, old, now):
		if not isinstance(now, QWidget): return
		if now != self and not isParentOfWidget(self, now): self.close()

	def pickScreenshotColor(self):
		def onPickedColorUpdate(color, finish):
			if not finish: return
			if self.currentColor != color:
				self.currentColor.setRgba(color.rgba())
				self.updateCurrentColor('screen_pick')
			if self.screenColorPickers:
				for popup in self.screenColorPickers.values(): popup.close()
				self.screenColorPickers.clear()

		for screen in QApplication.screens():
			popup = ScreenColorPicker(screen, self.currentColor, onPickedColorUpdate, self.colorRing)
			self.screenColorPickers[ screen ] = popup
			popup.show()

	def updateCurrentColor(self, reason):
		self.colorChanged.emit(self.currentColor, reason)

	def updateColorSpace(self, space):
		if ColorPicker.ColorSpace == space: return
		ColorPicker.ColorSpace = space
		if space == _ColorSpaceHsv:
			self.colorCpt1.updateComponent(_ColorComponentEdit.CptH)
			self.colorCpt2.updateComponent(_ColorComponentEdit.CptS)
			self.colorCpt3.updateComponent(_ColorComponentEdit.CptV)
			self.colorCptA.updateLineEdit()
		else:
			self.colorCpt1.updateComponent(_ColorComponentEdit.CptR)
			self.colorCpt2.updateComponent(_ColorComponentEdit.CptG)
			self.colorCpt3.updateComponent(_ColorComponentEdit.CptB)
			self.colorCptA.updateLineEdit()

	def revertColor(self):
		self.currentColor.setRgba(self.initColor.rgba())
		self.updateCurrentColor('revert')

	def keyPressEvent(self, evt):
		if self.screenColorPickers:
			for popup in self.screenColorPickers.values():
				if popup.underMouse(): return popup.keyPressEvent(evt)
		if evt.key() == Qt.Key_Escape: self.close()
		super().keyPressEvent(evt)

class ScreenColorPicker(QWidget):
	colorUpdated = Signal(QColor, bool)

	def __init__(self, screen, defaultColor, onColorUpdate, overridePaint = None):
		super().__init__()
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint | Qt.WindowStaysOnTopHint)
		self.setGeometry(screen.geometry())
		self.screenOffset = self.pos()
		self.screenshot = self.grabScreen(screen).toImage()
		self.defaultColor = QColor(defaultColor)

		self.setMouseTracking(False)
		if onColorUpdate: self.colorUpdated.connect(onColorUpdate)
		self.overridePaint = overridePaint

	def enterEvent(self, evt):
		super().enterEvent(evt)
		self.setMouseTracking(True)
		if self.overridePaint: self.overridePaint.overridePaintFunc = self.drawPreview
		self.onMouseMove(QCursor.pos() - self.screenOffset)

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		self.setMouseTracking(False)
		self.repaint()

	def closeEvent(self, evt):
		super().closeEvent(evt)
		if not self.overridePaint: return
		self.overridePaint.overridePaintFunc = None
		self.overridePaint.update()

	def grabScreen(self, screen):
		size = self.size()
		final = QPixmap(size)
		painter = QPainter(final)
		rect = QRect(0, 0, size.width(), size.height())
		screenshot = screen.grabWindow()
		painter.drawPixmap(rect, screenshot)
		return final

	def screenshotColorAt(self, pos):
		pos.setX(clamp(pos.x(), 0, self.width() - 1))
		pos.setY(clamp(pos.y(), 0, self.height() - 1))
		return self.screenshot.pixelColor(pos)

	# can not invoked from event system with window type Qt::ToolTip,
	# let corresponding ColorPicker redirect its key event to here...
	def keyPressEvent(self, evt):
		key = evt.key()
		if key == Qt.Key_Escape:
			self.colorUpdated.emit(self.defaultColor, True)
			self.close()

	def mousePressEvent(self, evt):
		btn = evt.button()
		if btn == Qt.RightButton:
			self.colorUpdated.emit(self.defaultColor, True)
			self.close()
		elif btn == Qt.MiddleButton:
			evt.ignore()
		else:
			color = self.screenshotColorAt(QCursor.pos() - self.screenOffset)
			self.colorUpdated.emit(color, True)
			self.close()

	def mouseMoveEvent(self, evt):
		self.onMouseMove(evt.pos())

	def onMouseMove(self, pos):
		if not self.underMouse(): return
		self.colorUpdated.emit(self.screenshotColorAt(pos), False)
		if self.overridePaint: self.overridePaint.update()
		self.update()

	def paintEvent(self, evt):
		rect = self.rect()
		painter = QPainter(self)
		painter.fillRect(rect, QColor(0, 0, 0, 1))

		if not self.underMouse(): return

		pos = QCursor.pos() - self.screenOffset
		px, py = pos.x(), pos.y()
		offset, size, halfSize = 20, 110, 55
		x, y = px + offset, py + offset
		w, h = rect.width(), rect.height()
		if x + size > w: x = px - offset - size
		if y + size > h - 30: y = py - offset - size
		painter.setPen(QColor('#0a0'))
		tarRect = QRect(x, y, size, size)
		srcRect = QRect(px - 5, py - 5, 10 + 1, 10 + 1)
		painter.drawImage(tarRect, self.screenshot, srcRect)
		painter.drawLine(x, y, x + size, y)
		painter.drawLine(x + size, y, x + size, y + size)
		painter.drawLine(x + size, y + size, x, y + size)
		painter.drawLine(x, y + size, x, y)
		painter.drawLine(x + halfSize, y, x + halfSize, y + size)
		painter.drawLine(x, y + halfSize, x + size, y + halfSize)

		pos = QCursor.pos() - self.screenOffset
		color = self.screenshotColorAt(pos).name().upper()
		fm = self.fontMetrics()
		width = fm.horizontalAdvance(color) + 8
		height = fm.height() + 4
		rect = QRect(x, y + size + 5, width, height)
		painter.fillRect(rect, Qt.black)
		painter.setPen(Qt.white)
		painter.drawText(rect, Qt.AlignCenter, color)


	def drawPreview(self, painter):
		margin = 11
		x, y = margin, margin
		size = self.overridePaint.width() - margin * 2
		
		pos = QCursor.pos() - self.screenOffset
		px, py = pos.x(), pos.y()
		painter.setPen(QColor(120, 120, 120, 160))
		srcRect = QRect(px - 10, py - 10, 20 + 1, 20 + 1)
		tarRect = QRect(x, y, size, size)
		painter.drawImage(tarRect, self.screenshot, srcRect)
		ds = size / (20 + 1)
		for i in range(20 + 2):
			d = round(i * ds)
			painter.drawLine(x, y + d, x + size, y + d)
			painter.drawLine(x + d, y, x + d, y + size)

		# painter.setPen(QColor('#080'))
		# d = size // 2
		# painter.drawLine(x, y + d, x + size, y + d)
		# painter.drawLine(x + d, y, x + d, y + size)

		painter.setPen(QColor('#080'))
		painter.setBrush(Qt.transparent)
		offset = round(10 * ds) - 1
		ids = round(ds) + 2
		painter.drawRect(x + offset, y + offset, ids, ids)
