from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem
from editor.models.basic_model import BasicModel
from editor.common.icon_cache import getThemePixmap
from editor.widgets.complex.tree_view import TreeView
from editor.view_manager import DockView, dockView


@dockView('Hierarchy', icon = 'hierarchy.png')
class HierarchyView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		tree = self.createTreeView(self)
		self.setWidget(tree)


	def createTreeView(self, parent):
		view = TreeView(parent)
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

		# model.dataChanged.connect(lambda i1, i2, r: print(r))
		view.setModel(model)
		return view
