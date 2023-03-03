from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QSplitter
from PySide6.QtGui import QStandardItemModel, QStandardItem
from editor.widgets.complex.tree_view import TreeView
from editor.common.icon_cache import getThemePixmap
from editor.view_manager import DockView, dockView


@dockView('Gallery')
class GalleryView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)

		# layout = QHBoxLayout()
		# layout.setAlignment(Qt.AlignTop)
		# self.layout().addLayout(layout)

		tree = self.createTreeView(self)
		placeHolder = QFrame(self)
		placeHolder.setMinimumWidth(150)

		splitter = QSplitter(self)
		splitter.addWidget(tree)
		splitter.addWidget(placeHolder)
		splitter.setOrientation(Qt.Horizontal)
		splitter.setChildrenCollapsible(False)
		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 3)

		self.setWidget(splitter)
		# self.layout().addWidget(splitter)

	def createTreeView(self, parent):
		view = TreeView(parent)
		# view.setWindowFlags(Qt.Window)
		model = QStandardItemModel()
		for i in range(5):
			n = QStandardItem(f'Item_{i}')
			model.appendRow(n)
			for j in range(4):
				c = QStandardItem(f'Child_{j}')
				n.appendRow(c)

		# model.dataChanged.connect(lambda i1, i2, r: print(r))
		view.setModel(model)
		return view

	def keyPressEvent(self, evt):
		key = evt.key()
		if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_Up or key == Qt.Key_Down:
			super().keyPressEvent(evt)

	def minimumSizeHint(self):
		return QSize(300, 100)

