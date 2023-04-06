from PySide6.QtCore import Property, QAbstractAnimation, QPropertyAnimation, QVariantAnimation, QParallelAnimationGroup, QEasingCurve, QPoint
from PySide6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect, QWidget

class SlidingStackedWidget(QStackedWidget):
	Left2Right, Right2Left = range(2)

	@Property(int)
	def duration(self):
		return self._duration
	@duration.setter
	def duration(self, value):
		self._duration = value

	def __init__(self, parent = None):
		super().__init__(parent)
		self._duration = 200
		self._enableFade = True
		self._enableWrap = True
		self._busy = False

	def addWidget(self, wgt):
		if self._enableFade:
			effect = QGraphicsOpacityEffect(wgt)
			effect.setOpacity(1)
			wgt.setGraphicsEffect(effect)
		super().addWidget(wgt)

	def insertWidget(self, idx, wgt):
		if self._enableFade:
			effect = QGraphicsOpacityEffect(wgt)
			effect.setOpacity(1)
			wgt.setGraphicsEffect(effect)
		super().insertWidget(idx, wgt)

	def initWidget(self):
		curr = self.currentWidget()
		self.setFixedHeight(curr.height())
		self.addWidget(QWidget())

	def slideInNext(self):
		now = self.currentIndex()
		if self._enableWrap or now < self.count() - 1:
			self.slideInIdx(now + 1)

	def slideInPrev(self):
		now = self.currentIndex()
		if self._enableWrap or now > 0:
			self.slideInIdx(now - 1)

	def slideInIdx(self, idx):
		count = self.count() - 1
		if idx > count - 1:
			wgt = self.widget(idx % count)
			self.slideInWgt(wgt, self.Right2Left)
		elif idx < 0:
			wgt = self.widget(idx % count)
			self.slideInWgt(wgt, self.Left2Right)
		else:
			wgt = self.widget(idx)
			self.slideInWgt(wgt, self.Right2Left if idx > self.currentIndex() else self.Left2Right)

	def slideInWgt(self, newWidget, direction):
		if self._busy: return
		
		currIdx = self.currentIndex()
		nextIdx = self.indexOf(newWidget)
		if currIdx == nextIdx: return
		self.setCurrentIndex(self.count() - 1)

		rect = self.frameRect()
		w, h = rect.width(), rect.height()

		wgtNext = self.widget(nextIdx)
		wgtCurr = self.widget(currIdx)
		dx = w if direction == self.Left2Right else -w
		# wgtNext.resize(wgtCurr.width(), wgtNext.height())
		wgtNext.move(-dx, 0)
		wgtNext.show()
		wgtCurr.show()

		animCurrPos = QPropertyAnimation(wgtCurr, b'pos')
		animCurrPos.setEasingCurve(QEasingCurve.OutQuad)
		animCurrPos.setDuration(self._duration)
		animCurrPos.setStartValue(QPoint(0, 0))
		animCurrPos.setEndValue(QPoint(dx, 0))

		animNextPos = QPropertyAnimation(wgtNext, b'pos')
		animNextPos.setEasingCurve(QEasingCurve.OutQuad)
		animNextPos.setDuration(self._duration)
		animNextPos.setStartValue(QPoint(-dx, 0))
		animNextPos.setEndValue(QPoint(0, 0))

		self.animGroup = QParallelAnimationGroup()
		self.animGroup.addAnimation(animCurrPos)
		self.animGroup.addAnimation(animNextPos)

		animHeight = QVariantAnimation(self)
		animHeight.setEasingCurve(QEasingCurve.OutQuad)
		animHeight.setDuration(self._duration)
		animHeight.setStartValue(wgtCurr.height())
		animHeight.setEndValue(wgtNext.height())
		animHeight.valueChanged.connect(lambda h: self.setFixedHeight(h))
		animHeight.valueChanged.connect(lambda: wgtNext.resize(self.width(), wgtNext.height()))
		self.animGroup.addAnimation(animHeight)

		if self._enableFade:
			wgtCurrEffect = wgtCurr.graphicsEffect()
			animCurrOp = QPropertyAnimation(wgtCurrEffect, b'opacity')
			animCurrOp.setDuration(self._duration)
			animCurrOp.setStartValue(1)
			animCurrOp.setEndValue(0)

			wgtNextEffect = wgtNext.graphicsEffect()
			animNextOp = QPropertyAnimation(wgtNextEffect, b'opacity')
			animNextOp.setDuration(self._duration)
			animNextOp.setStartValue(0)
			animNextOp.setEndValue(1)

			self.animGroup.addAnimation(animCurrOp)
			self.animGroup.addAnimation(animNextOp)

		self.animGroup.finished.connect(lambda: self.onAnimationFinish(nextIdx))
		self.animGroup.start(QAbstractAnimation.DeleteWhenStopped)
		self._busy = True

	def onAnimationFinish(self, nextIdx):
		self.setCurrentIndex(nextIdx)
		self._busy = False
