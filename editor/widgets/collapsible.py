from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CollapsibleWidget(QWidget):
	Expanded, Collapsed, Animating = range(3) # states

	def __init__(self, parent = None, expanded = True):
		super().__init__(parent)
		self.widget = None
		self.animation = None
		self.animating = True
		# self.animating = False
		self.animatingDuration = 120
		if expanded:
			self.state = self.Expanded
			self.show()
		else:
			self.state = self.Collapsed
			self.hide()

		layout = QVBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(layout)

	def setWidget(self, widget):
		if self.widget:
			self.layout().takeWidget()
			self.widget.deleteLater()
		self.layout().addWidget(widget)
		wl = widget.layout()
		if wl: wl.setSizeConstraint(QLayout.SetMinAndMaxSize)
		# widget.setFixedHeight(widget.sizeHint().height())
		self.widget = widget

		def takeWidget(self):
			if self.widget: self.layout().takeWidget()
			return self.widget

	def toggle(self):
		if self.state == self.Expanded:
			self.collapse()
		elif self.state == self.Collapsed:
			self.expand()

	def collapse(self):
		if not self.widget: return
		if self.state != self.Expanded: return
		if self.animating:
			self.state = self.Animating
			anim = QVariantAnimation(self)
			anim.setDuration(self.animatingDuration)
			anim.setStartValue(self.widget.sizeHint().height())
			anim.setEndValue(0)
			anim.setEasingCurve(QEasingCurve.InOutQuad)
			anim.valueChanged.connect(self.tickAnimating)
			anim.finished.connect(self.onCollapseFinish)
			anim.start()
			self.animation = anim
		else:
			self.hide()
			self.state = self.Collapsed

	def expand(self):
		if not self.widget: return
		if self.state != self.Collapsed: return
		if self.animating:
			self.setFixedHeight(0)
			self.show()
			self.state = self.Animating
			anim = QVariantAnimation(self)
			anim.setDuration(self.animatingDuration)
			anim.setStartValue(0)
			anim.setEndValue(self.widget.sizeHint().height())
			anim.setEasingCurve(QEasingCurve.InOutQuad)
			anim.valueChanged.connect(self.tickAnimating)
			anim.finished.connect(self.onExpandFinish)
			anim.start()
			self.animation = anim
		else:
			self.show()
			self.state = self.Expanded

	def tickAnimating(self, value):
		self.setFixedHeight(value)
		self.update()

	def onCollapseFinish(self):
		self.state = self.Collapsed
		self.animation.deleteLater()
		self.animation = None
		self.setFixedHeight(0)
		self.hide()

	def onExpandFinish(self):
		self.state = self.Expanded
		self.animation.deleteLater()
		self.animation = None

	# def paintEvent(self, e):
	# 	if self.state != self.Animating: return super().paintEvent(e)
	# 	painter = QPainter(self)
	# 	pixmap = self.widget.grab()
	# 	rect = self.widget.geometry()
	# 	painter.drawPixmap(rect, pixmap)
