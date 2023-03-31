from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QCursor
from editor.view_manager import DockView, dockView
from editor.widgets.complex.color_picker import ColorPicker


@dockView('TestRunner')
class TestRunnerView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		self.layout().addLayout(layout)

		btn1 = QPushButton("Test ColorPicker", self)
		btn1.clicked.connect(lambda: ColorPicker('#5D99E6').show())
		layout.addWidget(btn1)

		btn2 = QPushButton("Test Notification", self)
		btn2.clicked.connect(lambda: self.showNotification('hello\nhello again'))
		layout.addWidget(btn2)

