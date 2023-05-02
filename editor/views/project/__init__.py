import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QSizePolicy
from editor.models.editor.asset_model import AssetModel, FolderModel, ItemType
from editor.widgets.basic.slider import Slider
from editor.widgets.basic.line_edit import SearchLineEdit
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.misc.breadcrumb import Breadcrumb
from editor.view_manager import DockView, dockView
from editor.common.icon_cache import getThemePixmap
from editor.common.math import lerp, locAt


class LayoutSlider(Slider):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.threshold = 0.2

	def validateValue(self):
		self.blockSignals(True)
		mini = self.minimum()
		maxi = self.maximum()
		value = self.value()
		if value < lerp(mini, maxi, self.threshold): self.setValue(mini)
		self.blockSignals(False)
		self.update()

	def mouseReleaseEvent(self, evt):
		super().mouseReleaseEvent(evt)
		self.validateValue()

	def keyReleaseEvent(self, evt):
		super().keyReleaseEvent(evt)
		self.validateValue()

	def normalizedValue(self):
		mini = self.minimum()
		maxi = self.maximum()
		value = self.value()
		begin = lerp(mini, maxi, self.threshold)
		return -1 if value < begin else locAt(begin, maxi, value)


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
		def currentChanged(current, previous):
			if not current.isValid(): return
			item = assetView.model().itemFromIndex(current)
			if item.itemType() != ItemType.Normal: return
			folderView.model().setFolder(item.itemData())
		assetView.selectionModel().currentChanged.connect(currentChanged)

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
		slider = LayoutSlider()
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
		view.expand(model.index(0, 0))
		view.expand(model.index(2, 0))
		return view

	def createFolderView(self, parent):
		view = TreeView(parent)
		model = FolderModel(True)
		view.setModel(model)

		base = os.environ[ 'DEAR_BASE_PATH' ]
		model.setFolder(base)
		return view
