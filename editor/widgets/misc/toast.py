from PySide6.QtCore import Qt, QTimer, QEvent, Property, QPropertyAnimation
from PySide6.QtGui import QFont, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from editor.common.math import lerpI, clamp

_toastFont = QFont('consolas', 13)

class Toast(QWidget):
	def __init__(self, parent, msg, duration = 2000):
		super(Toast, self).__init__(parent)
		self.msg = msg
		self.duration = duration
		self._alpha = 220
		QTimer.singleShot(self.duration, self.fadeToast)

		parent.installEventFilter(self)
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		# self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_DeleteOnClose)
		self.moveCenter()

	@Property(int)
	def alpha(self):
		return self._alpha

	@alpha.setter
	def alpha(self, value):
		self._alpha = value
		self.update()

	def fadeToast(self):
		self.anim = QPropertyAnimation(self, b'alpha')
		self.anim.finished.connect(self.onFadeFinish)
		self.anim.setStartValue(self._alpha)
		self.anim.setDuration(800)
		self.anim.setEndValue(0)
		self.anim.start()
		
	def onFadeFinish(self):
		self.anim.deleteLater()
		self.parent().removeEventFilter(self)
		self.close()

	def eventFilter(self, obj, e):
		if e.type() == QEvent.Resize: self.moveCenter()
		return False

	def paintEvent(self, a0):
		rect = self.rect()
		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing, True)
		painter.setBrush(QBrush(QColor(100, 100, 100, self._alpha)))
		painter.setPen(Qt.transparent)
		painter.drawRoundedRect(rect, 15, 15)
		painter.setPen(QColor(230, 230, 230, self._alpha))
		painter.setFont(_toastFont)
		painter.drawText(rect, Qt.AlignCenter, self.msg)

	def moveCenter(self):
		rect = self.parent().rect()
		pw, ph = rect.width(), rect.height()
		sw = clamp(pw * 0.7, 100, 400)
		sh = clamp(ph * 0.4, 40 , 160)
		self.setFixedSize(sw, sh)

		offsetToBottom = ph * 0.15
		xPos = int((pw - sw)/2)
		yPos = int(ph - sh - offsetToBottom)
		self.move(xPos, yPos)

def notifyToast(host, msg, duration):
	toast = Toast(host, msg, duration)
	toast.show()
	return toast
	