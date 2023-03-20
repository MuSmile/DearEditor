from PySide6.QtCore import Qt, QTimer, QEvent, Property, QVariantAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPalette
from PySide6.QtWidgets import QWidget
from editor.common.math import clamp

class Toast(QWidget):
	@Property(int)
	def fadeDuration(self):
		return self._fadeDuration
	@fadeDuration.setter
	def fadeDuration(self, value):
		self._fadeDuration = value

	@Property(int)
	def toastRadius(self):
		return self._toastRadius
	@toastRadius.setter
	def toastRadius(self, value):
		self._toastRadius = value

	def __init__(self, text, parent):
		super().__init__(parent)
		self._text = text
		self._toastRadius = 15
		self._fadeDuration = 800
		self._opacity = 220

		QTimer.singleShot(2000, self.fadeToast)
		parent.installEventFilter(self)

		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.moveCenter()

	def tickFading(self, value):
		self._opacity = value
		self.update()

	def fadeToast(self):
		self.anim = QVariantAnimation(self)
		self.anim.finished.connect(self.onFadeFinish)
		self.anim.valueChanged.connect(self.tickFading)
		self.anim.setEasingCurve(QEasingCurve.InOutQuad)
		self.anim.setStartValue(self._opacity)
		self.anim.setEndValue(0)
		self.anim.setDuration(self._fadeDuration)
		self.anim.start()
		
	def onFadeFinish(self):
		self.anim.deleteLater()
		self.parent().removeEventFilter(self)
		self.close()

	def eventFilter(self, obj, evt):
		if evt.type() == QEvent.Resize: self.moveCenter()
		return False

	def paintEvent(self, evt):
		rect = self.rect()
		palette = self.palette()
		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing, True)
		painter.setRenderHints(QPainter.TextAntialiasing, True)
		background = palette.color(QPalette.Base)
		background.setAlpha(self._opacity)
		painter.setBrush(background)
		painter.setPen(Qt.transparent)
		painter.drawRoundedRect(rect, self._toastRadius, self._toastRadius)
		foreground = palette.color(QPalette.Text)
		foreground.setAlpha(self._opacity)
		painter.setPen(foreground)
		painter.setFont(self.font())
		painter.drawText(rect, Qt.AlignCenter, self._text)

	def moveCenter(self):
		rect = self.parent().rect()
		pw, ph = rect.width(), rect.height()
		sw = clamp(pw * 0.7, 100, 400)
		sh = clamp(ph * 0.4, 40 , 160)
		self.setFixedSize(sw, sh)

		offsetToBottom = ph * 0.15
		xPos = round((pw - sw) / 2)
		yPos = round(ph - sh - offsetToBottom)
		self.move(xPos, yPos)
