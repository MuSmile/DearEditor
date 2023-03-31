import sys
from PySide6.QtCore import Qt, Property, QVariantAnimation, QAbstractAnimation, QEasingCurve
from PySide6.QtWidgets import QScrollArea

class CollapsibleWidget(QScrollArea):
	@Property(int)
	def duration(self):
		return self._duration
	@duration.setter
	def duration(self, value):
		self._duration = value
		self._animation.setDuration(value)

	def __init__(self, parent = None):
		super().__init__(parent)
		self._duration = 100
		self._expanded = True
		self._animation = self.createAnim()

		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setWidgetResizable(False)

	def createAnim(self):
		anim = QVariantAnimation(self)
		anim.setDuration(self._duration)
		anim.setEasingCurve(QEasingCurve.InOutQuad)
		anim.valueChanged.connect(self.tickAnimating)
		return anim

	def tickAnimating(self, value):
		self.setFixedHeight(value)
		# self.update()

	def resizeEvent(self, evt):
		super().resizeEvent(evt)
		wgt = self.widget()
		if not wgt: return
		wgt.setFixedWidth(evt.size().width())

	def wheelEvent(self, evt):
		evt.ignore()

	def toggle(self):
		if self._expanded:
			self.collapse()
		else:
			self.expand()

	def collapse(self):
		self._expanded = False
		anim = self._animation
		if anim.state() == QAbstractAnimation.Running: anim.stop()
		anim.setStartValue(self.height())
		anim.setEndValue(0)
		anim.start()

	def expand(self):
		self._expanded = True
		anim = self._animation
		if anim.state() == QAbstractAnimation.Running: anim.stop()
		anim.setStartValue(self.height())
		anim.setEndValue(self.preferredHeight())
		anim.start()

	def collapseInstant(self):
		anim = self._animation
		if anim.state() == QAbstractAnimation.Running: anim.stop()
		self.setFixedHeight(0)

	def expandInstant(self):
		anim = self._animation
		if anim.state() == QAbstractAnimation.Running: anim.stop()
		self.setFixedHeight(self.preferredHeight())

	def preferredHeight(self):
		wgt = self.widget()
		if wgt: return wgt.sizeHint().height()
		else: return self.sizeHint().height()

	def updateFixedHeight(self):
		self.setFixedHeight(self.preferredHeight())
