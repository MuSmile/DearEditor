from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QStatusBar, QPushButton, QProgressBar, QLabel, QHBoxLayout
from editor.common.icon_cache import getThemeIcon, getEmptyIcon

def _createStatusProgressBar():
	label = QLabel()
	label.setAlignment(Qt.AlignRight)
	progressBar = QProgressBar()
	progressBar.setTextVisible(False)

	widget = QWidget()
	layout = QHBoxLayout()
	layout.setSpacing(12)
	layout.setContentsMargins(0, 0, 0, 0)
	layout.addWidget(label)
	layout.addWidget(progressBar)
	widget.setLayout(layout)
	return widget, label, progressBar

class MainStatusBar(QStatusBar):
	def __init__(self, parent = None):
		super().__init__(parent)
		self._setupOutputMsgWidget()
		self._setupProgressMsgWidget()
		self.clearOutputMsg()
		self.clearProgressMsg()
		self.messageChanged.connect(self._onNativeMsgChanged)

	def _onNativeMsgChanged(self, msg):
		if msg:
			if self.outputMsg.isVisible():
				self.cachedMsg  = self.outputMsg.text()
				self.cachedIcon = self.outputMsg.icon()
			self.showOutputMsg(msg)
		else:
			if self.cachedMsg:
				self.showOutputMsg(self.cachedMsg, self.cachedIcon)
				self.cachedMsg  = None
				self.cachedIcon = None
			else:
				self.clearOutputMsg()

	def _setupOutputMsgWidget(self):
		widget = QPushButton()
		widget.setStyleSheet('text-align: left;')
		widget.setFocusPolicy(Qt.NoFocus)
		self.addPermanentWidget(widget, 2)
		self.outputMsg = widget
		self.outputPressed = None
		self.cachedMsg  = None
		self.cachedIcon = None

	def _setupProgressMsgWidget(self):
		widget, label, progress = _createStatusProgressBar()
		self.addPermanentWidget(widget, 1)
		self.progress = progress
		self.progressLabel = label

	def showOutputMsg(self, msg, icon = None, pressed = None):
		self.outputMsg.setText(msg)
		self.outputMsg.setIcon(icon or getEmptyIcon())
		if pressed:
			self.outputPressed = pressed
			self.outputMsg.pressed.connect(pressed)
		self.outputMsg.setVisible(True)

	def clearOutputMsg(self):
		self.outputMsg.setVisible(False)
		if self.outputPressed:
			self.outputMsg.pressed.disconnect(self.outputPressed)
			self.outputPressed = None

	def showProgressMsg(self, msg, progress):
		self.progress.setValue(progress)
		self.progressLabel.setText(msg)
		self.progress.setVisible(True)
		self.progressLabel.setVisible(True)

	def clearProgressMsg(self):
		self.progress.setVisible(False)
		self.progressLabel.setVisible(False)
		self.progress.setValue(0)

def createMainStatusBar(parent = None):
	statusbar = MainStatusBar(parent)
	# statusbar.setSizeGripEnabled(False)

	# text = 'This is a test output log.'
	# icon = getThemeIcon('console.infoicon.sml.png')
	# statusbar.showOutputMsg(text, icon, lambda:print('hello'))

	# label = 'Auto generating'
	# t = QTimer(statusbar)
	# def counter():
	# 	v = statusbar.progress.value() + 1
	# 	v = v % 100
	# 	statusbar.showProgressMsg(label, v)
	# 	# if v >= 100:
	# 	# 	t.stop()
	# 	# 	statusbar.clearProgressMsg()
	# t.timeout.connect(counter)
	# t.start(20)

	return statusbar
