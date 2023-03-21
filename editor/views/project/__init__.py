import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QFileSystemModel, QTreeView
from editor.common.icon_cache import getThemePixmap
from editor.widgets.complex.tree_view import TreeView
from editor.view_manager import DockView, dockView
from editor.models.editor.file_system import FileSystemModel


@dockView('Project', icon = 'project.png')
class ProjectView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		tree = self.createTreeView(self)
		self.setWidget(tree)


	def createTreeView(self, parent):
		view = TreeView(parent)
		base = os.environ[ 'DEAR_BASE_PATH' ]
		model = FileSystemModel(base)
	
		# for i in range(5):
		# 	n = QStandardItem(f'Item_{i}')
		# 	n.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
		# 	model.appendRow(n)
		# 	for j in range(4):
		# 		c = QStandardItem(f'Child_{j}')
		# 		c.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
		# 		n.appendRow(c)
		# 		for k in range(4):
		# 			s = QStandardItem(f'Subchild_{k}')
		# 			# s.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
		# 			c.appendRow(s)

		view.setModel(model)
		return view
