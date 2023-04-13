import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSplitter, QVBoxLayout, QHBoxLayout
from editor.models.editor.file_system import FileSystemModel, FolderContentModel
from editor.widgets.basic.line_edit import SearchLineEdit
from editor.widgets.complex.tree_view import TreeView
from editor.view_manager import DockView, dockView


@dockView('Project', icon = 'project.png')
class ProjectView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)

		layout = QVBoxLayout()
		self.layout().addLayout(layout)

		searchbar = QWidget(self)
		searchbar.setFixedHeight(24)
		searchbar.setObjectName('searchbar')
		searchbarLayout = QHBoxLayout(searchbar)
		searchbarLayout.setContentsMargins(0, 2, 2, 4)
		searchbarLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout.addWidget(searchbar)

		searchEdit = SearchLineEdit(self)
		searchEdit.setFixedWidth(320)
		searchbarLayout.addWidget(searchEdit)

		
		splitter = QSplitter(self)
		tree = self.createTreeView(self)
		treeR = self.createRightTreeView(self)

		splitter.addWidget(tree)
		splitter.addWidget(treeR)

		splitter.setOrientation(Qt.Horizontal)
		splitter.setChildrenCollapsible(False)
		splitter.setSizes([100, 200])

		layout.addWidget(splitter)


	def createTreeView(self, parent):
		view = TreeView(parent)
		model = FileSystemModel(True)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.addPath(base)
		# view.expandAll()
		view.expand(model.index(0, 0))
		view.expand(model.index(2, 0))
		return view

	def createRightTreeView(self, parent):
		view = TreeView(parent)
		model = FolderContentModel(True)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.setFolder(base)
		# view.expandAll()
		# view.setRootIndex(model.index(0, 0))
		return view
