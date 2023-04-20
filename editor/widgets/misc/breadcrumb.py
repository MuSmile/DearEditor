from PySide6.QtCore import Qt, QRect, Property
from PySide6.QtGui import QPainter, QPalette
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from editor.common.math import clamp

class Breadcrumb(QWidget):
	def __init__(self, pathList, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignLeft)
		layout.setContentsMargins(4, 2, 2, 2)
		layout.setSpacing(0)
		self.setLayout(layout)
		self.setPathList(pathList)

	def setPathList(self, pathList):
		# self.pathList = pathList
		
		layout = self.layout()
		for i in range(layout.count()):
			item = layout.takeAt(0)
			item.widget().deleteLater()
		
		layout.addWidget(self.createPathBtn(pathList[0]))
		for i in range(1, len(pathList)):
			layout.addWidget(self.createSeparatorBtn())
			layout.addWidget(self.createPathBtn(pathList[i]))

		last = layout.count() - 1
		layout.itemAt(last).widget().setObjectName('current')

	def createPathBtn(self, path):
		btn = QPushButton(path, self)
		btn.setObjectName('path')
		return btn

	def createSeparatorBtn(self):
		btn = QPushButton('>', self)
		btn.setObjectName('separator')
		return btn