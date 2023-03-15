from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QCursor
from editor.view_manager import DockView, dockView
from editor.widgets.complex.tree_view import runTreeDemo
from editor.widgets.complex.color_picker import createColorPicker


class MyPopup(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowFlag(Qt.Popup, True)
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.setWindowFlag(Qt.NoDropShadowWindowHint, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		# self.setWindowOpacity(0.1)
		# self.setStyleSheet('QWidget { background-color: transparent; }')
		self.btn = QPushButton('test', self)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.btn.resize(self.width(), self.height())


@dockView('Project', icon = 'project.png')
class ProjectView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		self.layout().addLayout(layout)

		btn1 = QPushButton("Test Tree", self)
		btn1.clicked.connect(runTreeDemo)
		layout.addWidget(btn1)

		btn2 = QPushButton("Test Popup", self)
		btn2.clicked.connect(self.doit)
		layout.addWidget(btn2)

		btn3 = QPushButton("Test ColorPicker", self)
		btn3.clicked.connect(lambda: createColorPicker('#5D99E6'))
		layout.addWidget(btn3)

		btn4 = QPushButton("Test Notification", self)
		btn4.clicked.connect(lambda: self.showNotification('hello\nhello again'))
		layout.addWidget(btn4)


	def doit(self):
		self.w = MyPopup()
		self.w.show()
		self.w.resize(200, 300)
		self.w.move(QCursor.pos())
