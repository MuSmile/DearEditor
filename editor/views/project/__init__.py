import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QSizePolicy
from editor.models.editor.asset_model import AssetModel, FolderModel
from editor.widgets.basic.slider import Slider
from editor.widgets.basic.line_edit import SearchLineEdit
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.misc.breadcrumb import Breadcrumb
from editor.view_manager import DockView, dockView
from editor.common.icon_cache import getThemePixmap


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
		assetView = self.createAssetView(self)
		folderView = self.createFolderView(self)

		breadcrumb = Breadcrumb(['Hello', 'World', 'Foo', 'BAR'], self)
		breadcrumb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		statusBar = QFrame(self)
		statusBar.setObjectName('statusbar')
		statusLayout = QHBoxLayout(statusBar)
		statusLayout.setContentsMargins(4, 0, 4, 0)
		statusLayout.setSpacing(2)

		icon = QLabel()
		icon.setPixmap(getThemePixmap('folder_close.png').scaled(16, 16))
		icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		label = QLabel('test/test/test.txt')
		label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		slider = Slider()
		slider.setFocusPolicy(Qt.ClickFocus)
		slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
		statusLayout.addWidget(icon)
		statusLayout.addWidget(label)
		statusLayout.addStretch()
		statusLayout.addWidget(slider)

		contentContainer = QWidget(self)
		contentLayout = QVBoxLayout(contentContainer)
		contentLayout.setContentsMargins(0, 0, 0, 0)
		contentLayout.setSpacing(0)
		contentLayout.addWidget(breadcrumb)
		contentLayout.addWidget(folderView)
		contentLayout.addWidget(statusBar)

		splitter.addWidget(assetView)
		splitter.addWidget(contentContainer)

		splitter.setOrientation(Qt.Horizontal)
		splitter.setChildrenCollapsible(False)
		splitter.setSizes([100, 200])

		layout.addWidget(splitter)

	def createAssetView(self, parent):
		view = TreeView(parent)
		model = AssetModel(True)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.addPath(base)
		# view.expandAll()
		view.expand(model.index(0, 0))
		view.expand(model.index(2, 0))
		return view

	def createFolderView(self, parent):
		view = TreeView(parent)
		model = FolderModel(True)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.setFolder(base)
		# view.expandAll()
		# view.setRootIndex(model.index(0, 0))
		return view
