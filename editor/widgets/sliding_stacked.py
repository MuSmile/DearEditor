from PySide6.QtCore import Signal, QAbstractAnimation, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QPoint
from PySide6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect

_Auto, _Left2Right, _Right2Left, _Top2Bottom, _Bottom2Top = range(5)

class SlidingStackedWidget(QStackedWidget):
	animationFinished = Signal()

	def __init__(self, parent = None):
		super().__init__(parent)
		self.duration = 500
		self.animationtype = QEasingCurve.OutQuad
		self.vertical = False
		self.wrap = False

		self.now  = 0
		self.next = 0
		self.pnow = QPoint(0, 0)
		self.active = False
		self.enableFade = True

		self.animgroup = None

	def setFadeEnable(self, enable):
		self.enableFade = enable

	def setSlidingDuration(self, duration = 500):
		self.duration = duration

	def setSlidingEase(self, ease):
		self.animationtype = ease

	def setVerticalSliding(self, vertical = False):
		self.vertical = vertical

	def slideInNext(self):
		now = self.currentIndex()
		if self.wrap or now < self.count() - 1:
			self.slideInIdx(now + 1)
			return True
		else:
			return False

	def slideInPrev(self):
		now = self.currentIndex()
		if self.wrap or now > 0:
			self.slideInIdx(now - 1)
			return True
		else:
			return False

	def slideInIdx(self, idx, direction = _Auto):
		count = self.count()
		if idx > count - 1:
			direction = self.vertical and _Top2Bottom or _Right2Left
			idx %= count
		elif idx < 0:
			direction = self.vertical and _Bottom2Top or _Left2Right
			idx %= count
		self.slideInWgt(self.widget(idx), direction)

	def slideInWgt(self, newWidget, direction = _Auto):
		if self.active: return
		self.active = True
		
		directionhint = None
		now = self.currentIndex()
		next = self.indexOf(newWidget)
		if now == next:
			self.active = False
			return
		elif now < next:
			directionhint = self.vertical and _Top2Bottom or _Right2Left
		else:
			directionhint = self.vertical and _Bottom2Top or _Left2Right

		if direction == _Auto: direction = directionhint

		rect = self.frameRect()
		offsetx = rect.width()
		offsety = rect.height()

		wgtNext = self.widget(next)
		wgtNow  = self.widget(now)
		wgtNext.setGeometry(0, 0, offsetx, offsety)
		if direction == _Bottom2Top:
			offsetx = 0
			offsety = -offsety
		elif direction == _Top2Bottom:
			offsetx = 0
		elif direction == _Right2Left:
			offsetx = -offsetx
			offsety = 0
		elif direction == _Left2Right:
			offsety = 0

		pnext = wgtNext.pos()
		pnow = wgtNow.pos()
		self.pnow = pnow
		wgtNext.move(pnext.x() - offsetx, pnext.y() - offsety)
		wgtNext.show()
		wgtNext.raise_()

		animnow = QPropertyAnimation(wgtNow, b'pos')
		animnow.setDuration(self.duration)
		animnow.setEasingCurve(self.animationtype)
		animnow.setStartValue(QPoint(pnow.x(), pnow.y()))
		animnow.setEndValue(QPoint(pnow.x() + offsetx, pnow.y() + offsety))

		animnext = QPropertyAnimation(wgtNext, b'pos')
		animnext.setDuration(self.duration)
		animnext.setEasingCurve(self.animationtype)
		animnext.setStartValue(QPoint(pnext.x() - offsetx, pnext.y() - offsety))
		animnext.setEndValue(QPoint(pnext.x(), pnext.y()))

		self.animgroup = QParallelAnimationGroup()
		self.animgroup.addAnimation(animnow)
		self.animgroup.addAnimation(animnext)

		if self.enableFade:
			animnow_op_eff = QGraphicsOpacityEffect()
			wgtNow.setGraphicsEffect(animnow_op_eff)

			animnow_op = QPropertyAnimation(animnow_op_eff, b'opacity')
			animnow_op.setDuration(self.duration)
			animnow_op.setStartValue(1)
			animnow_op.setEndValue(0.2)
			def animnow_cb():
				if animnow_op_eff: animnow_op_eff.deleteLater()
			animnow_op.finished.connect(animnow_cb)

			animnext_op_eff = QGraphicsOpacityEffect()
			animnext_op_eff.setOpacity(0)
			wgtNext.setGraphicsEffect(animnext_op_eff)

			animnext_op = QPropertyAnimation(animnext_op_eff, b'opacity')
			animnext_op.setDuration(self.duration)
			animnext_op.setStartValue(0.8)
			animnext_op.setEndValue(1)
			def animnext_cb():
				if animnext_op_eff: animnext_op_eff.deleteLater()
			animnext_op.finished.connect(animnext_cb)
			self.animgroup.addAnimation(animnow_op)
			self.animgroup.addAnimation(animnext_op)

		self.next = next
		self.now = now
		self.active = True
		self.animgroup.finished.connect(self.onAnimationFinish)
		self.animgroup.start(QAbstractAnimation.DeleteWhenStopped)

	def onAnimationFinish(self):
		self.setCurrentIndex(self.next)
		currwgt = self.widget(self.now)
		currwgt.hide()
		currwgt.move(self.pnow)
		self.active = False
		self.animationFinished.emit()

if __name__ == '__main__':
	import sys
	from PySide6.QtWidgets import QWidget, QPushButton, QApplication

	app = QApplication(sys.argv)
	demo = QWidget()
	demo.resize(500, 400)
	ssw = SlidingStackedWidget(demo)
	ssw.setGeometry(50, 50, 400, 200)

	w1 = QPushButton('Page 1')
	w2 = QPushButton('Page 2')
	w3 = QPushButton('Page 3')
	w1.setStyleSheet("background-color: blue ; border: 0; font-size: 24px; color: white;")
	w2.setStyleSheet("background-color: green; border: 0; font-size: 24px; color: white;")
	w3.setStyleSheet("background-color: gray ; border: 0; font-size: 24px; color: white;")
	ssw.addWidget(w1)
	ssw.addWidget(w2)
	ssw.addWidget(w3)
	w2.setFixedHeight(100)
	# ssw.vertical = True
	ssw.wrap = True

	btn1 = QPushButton('Prev', demo)
	btn1.setGeometry(0, 320, 200, 80)
	btn1.clicked.connect(ssw.slideInPrev)

	btn2 = QPushButton('Next', demo)
	btn2.setGeometry(300, 320, 200, 80)
	btn2.clicked.connect(ssw.slideInNext)

	demo.show()
	sys.exit(app.exec())
