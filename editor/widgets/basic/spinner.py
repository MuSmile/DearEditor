from PySide6.QtCore import QSize, QTimer, Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

class WaitingSpinner(QWidget):
	def __init__(self, parent = None, color = None, spinnerCount = 13, rotateSpeed = 1.5, clockwise = True):
		super().__init__(parent)
		self.angle = 0

		self.color = color or QColor(200, 200, 200)
		self.spinnerCount = spinnerCount
		self.clockwise = clockwise

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateAngle)
		self.timerInterval = round(1000 / rotateSpeed / self.spinnerCount)

	def showEvent(self, evt):
		super().showEvent(evt)
		self.timer.start(self.timerInterval)

	def hideEvent(self, evt):
		super().hideEvent(evt)
		self.timer.stop()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.translate(self.width() / 2, self.height() / 2)
		scale = min(self.width(), self.height()) / 100
		painter.scale(scale, scale)
		painter.rotate(self.angle)
		painter.setPen(Qt.NoPen)
		offset = 22
		for i in range(self.spinnerCount):
			self.color.setAlphaF(i / (self.spinnerCount - 1))
			painter.setBrush(self.color)
			rect = QRectF(offset, -50/self.spinnerCount, 50 - offset, 1.2 * 100/self.spinnerCount)
			painter.drawRoundedRect(rect, 6, 6)
			painter.rotate(360 / self.spinnerCount)

	def updateAngle(self):
		delta = 360 / self.spinnerCount
		self.angle += self.clockwise and delta or -delta
		self.angle %= 360
		self.update()

	def sizeHint(self):
		return QSize(100, 100)

class CircleSpinner(QWidget):
	def __init__(self, parent = None, circleColor = None, arcColor = None, rotateInterval = 33, rotateStep = 10, spanAngle = 80, clockwise = True):
		super().__init__(parent)
		self.angle = 0
		self.circleWidth = 4

		self.circleColor = circleColor or QColor(120, 120, 120)
		self.arcColor = arcColor or QColor(200, 200, 200)
		self.clockwise = clockwise

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateAngle)
		self.rotateStep = rotateStep
		self.rotateInterval = rotateInterval
		self.spanAngle = spanAngle

	def showEvent(self, evt):
		super().showEvent(evt)
		self.timer.start(self.rotateInterval)

	def hideEvent(self, evt):
		super().hideEvent(evt)
		self.timer.stop()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		w = self.circleWidth
		rect = self.rect().adjusted(w, w, -w, -w)
		painter.setPen(QPen(self.circleColor, w))
		painter.drawEllipse(rect)
		painter.setPen(QPen(self.arcColor, w))
		painter.drawArc(rect, self.angle * 16, self.spanAngle * 16)

	def updateAngle(self):
		delta = self.rotateStep
		self.angle += self.clockwise and delta or -delta
		self.angle %= 360
		self.update()

	def sizeHint(self):
		return QSize(100, 100)

if __name__ == '__main__':
	import sys
	from PySide6.QtWidgets import QApplication, QHBoxLayout

	app = QApplication(sys.argv)
	w = QWidget()
	layout = QHBoxLayout(w)
	layout.addWidget(WaitingSpinner(w))
	layout.addWidget(WaitingSpinner(w, QColor(50, 120, 200), clockwise = False))
	layout.addWidget(WaitingSpinner(w))
	w.show()
	sys.exit(app.exec())
	