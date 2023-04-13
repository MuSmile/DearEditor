from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QCursor, QStandardItem
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from editor.models.basic_model import BasicModel
from editor.common.icon_cache import getThemePixmap
from editor.widgets.complex.color_picker import ColorPicker
from editor.widgets.complex.tree_view import TreeView
from editor.view_manager import DockView, dockView


@dockView('TestRunner')
class TestRunnerView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		
		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		self.layout().addLayout(layout)

		btn1 = QPushButton("Test TreeView", self)
		btn1.clicked.connect(self.createTreeView)
		layout.addWidget(btn1)

		btn2 = QPushButton("Test ColorPicker", self)
		btn2.clicked.connect(lambda: ColorPicker('#5D99E6').show())
		layout.addWidget(btn2)

		btn23 = QPushButton("Test Notification", self)
		btn23.clicked.connect(lambda: self.showNotification('hello\nhello again'))
		layout.addWidget(btn23)


	def createTreeView(self):
		view = TreeView(self)
		model = BasicModel()
		for i in range(5):
			n = QStandardItem(f'Item_{i}')
			n.setData(getThemePixmap('entity.png'), Qt.DecorationRole)
			model.appendRow(n)
			for j in range(4):
				c = QStandardItem(f'Child_{j}')
				c.setData(getThemePixmap('entity.png'), Qt.DecorationRole)
				n.appendRow(c)
				for k in range(4):
					s = QStandardItem(f'Subchild_{k}')
					# s.setData(getThemePixmap('entity.png'), Qt.DecorationRole)
					c.appendRow(s)

		view.setModel(model)
		view.setWindowFlag(Qt.Window)
		view.show()
