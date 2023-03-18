from PySide6.QtCore import QSize, QTimer, Qt, QRectF
from PySide6.QtGui import QColor, QPainter
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
		self.timer.start(round(1000 / rotateSpeed / self.spinnerCount))

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.translate(self.width() / 2, self.height() / 2)
		side = min(self.width(), self.height())
		painter.scale(side / 100.0, side / 100.0)
		painter.rotate(self.angle)
		painter.save()
		painter.setPen(Qt.NoPen)
		color = self.color.toRgb()
		for i in range(self.spinnerCount):
			color.setAlphaF(1.0 * i / (self.spinnerCount - 1))
			painter.setBrush(color)
			# painter.drawEllipse(30, -10, 20, 20)
			offset = 22
			rect = QRectF(offset, -50/self.spinnerCount, 50 - offset, 1.2 * 100/self.spinnerCount)
			painter.drawRoundedRect(rect, 6, 6)
			painter.rotate(360 / self.spinnerCount)
		painter.restore()

	def updateAngle(self):
		delta = 360 / self.spinnerCount
		self.angle += self.clockwise and delta or -delta
		self.angle %= 360
		self.update()

	def sizeHint(self) -> QSize:
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
	