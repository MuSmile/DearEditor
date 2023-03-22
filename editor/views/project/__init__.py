import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView
from editor.models.editor.file_system import FileSystemModel
from editor.widgets.complex.tree_view import TreeView
from editor.view_manager import DockView, dockView


@dockView('Project', icon = 'project.png')
class ProjectView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		tree = self.createTreeView(self)
		self.setWidget(tree)


	def createTreeView(self, parent):
		view = TreeView(parent)
		model = FileSystemModel(True, False)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.addRootItem(base)
		view.expand(model.index(0, 0))
		return view
