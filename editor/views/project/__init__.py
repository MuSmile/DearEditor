from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QWidget, QPushButton
from editor.view_manager import DockView, dockView
from editor.widgets.complex.tree_view import runTreeDemo


class MyPopup(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowFlag(Qt.Popup, True)
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		# self.setWindowOpacity(0.1)
		# self.setStyleSheet('QWidget { background-color: transparent; }')
		btn = QPushButton('test', self)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		btn.resize(self.width(), self.height())


@dockView('Project', icon = 'project.png')
class ProjectView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		btn = QPushButton("Click me", self)
		btn.setGeometry(QRect(0, 0, 100, 30))
		btn.clicked.connect(runTreeDemo)
		# btn.clicked.connect(self.doit)
 
		self.setWidget(btn)

	def doit(self):
		self.w = MyPopup()
		self.w.show()
		self.w.resize(200, 300)
		self.w.move(QCursor.pos())
