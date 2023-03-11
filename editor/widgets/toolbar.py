from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QMenu, QToolBar, QToolButton, QPushButton, QButtonGroup, QHBoxLayout, QGridLayout, QSizePolicy
from editor.widgets.basic.button import CheckableToolButton, IconTextToolButton, ToggleableToolButton, PopupPushButton, PopupToolButton
from editor.common.icon_cache import getThemeIcon

class ToolButtonGroup(QWidget):
	def __init__(self, exclusive = True):
		super().__init__()
		self.group = QButtonGroup()
		self.group.setExclusive(exclusive)
		self.layout = QHBoxLayout()
		self.layout.setSpacing(1)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)

	def addButton(self, button):
		self.layout.addWidget(button)
		self.group.addButton(button)

class ToolBarContainer(QWidget):
	def __init__(self, alignment, spacing):
		super().__init__()
		layout = QHBoxLayout()
		layout.setSpacing(spacing)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setAlignment(alignment)
		self.setLayout(layout)

class _ToolBarImpl(QWidget):
	def __init__(self):
		super().__init__()
		self.containerL = ToolBarContainer(Qt.AlignLeft  , 7)
		self.containerM = ToolBarContainer(Qt.AlignCenter, 1)
		self.containerR = ToolBarContainer(Qt.AlignRight , 7)
		self.containerL.setObjectName('Left')
		self.containerM.setObjectName('Center')
		self.containerR.setObjectName('Right')
		self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

		grid = QGridLayout()
		grid.addWidget(self.containerL, 0, 0, 1, 3)
		grid.addWidget(self.containerM, 0, 3, 1, 1)
		grid.addWidget(self.containerR, 0, 4, 1, 3)
		grid.setSpacing(10)
		grid.setContentsMargins(0, 0, 0, 0)

		self.setLayout(grid)

	def addLeftWidget(self, widget):
		self.containerL.layout().addWidget(widget)

	def addRightWidget(self, widget):
		self.containerR.layout().addWidget(widget)

	def addCenterWidget(self, widget):
		self.containerM.layout().addWidget(widget)

def _createToolBarImpl():
	toolbar = _ToolBarImpl()

	btnSearch = QToolButton()
	btnSearch.setIcon(getThemeIcon('search.png'))
	btnSearch.setFixedWidth(22)

	btnBuild = IconTextToolButton('Build', 'build.png')
	btnLayer = PopupPushButton('Layer')
	btnLayer.addTestMenu()
	btnLayout = PopupPushButton('Layout')
	btnLayout.addTestMenu()

	# test = PopupToolButton('Test')
	# test.addTestMenu()

	toolbar.addRightWidget(btnBuild)
	# toolbar.addRightWidget(test)
	toolbar.addRightWidget(btnLayer)
	toolbar.addRightWidget(btnLayout)
	toolbar.addRightWidget(btnSearch)

	# init left widgets
	btnViewMove = CheckableToolButton('tool_viewmove.png')
	btnMove = CheckableToolButton('tool_move.png')
	btnRotate = CheckableToolButton('tool_rotate.png')
	btnScale = CheckableToolButton('tool_scale.png')
	btnRect = CheckableToolButton('tool_rect.png')
	btnViewMove.setChecked(True)

	toolGroup = ToolButtonGroup()
	toolGroup.addButton(btnViewMove)
	toolGroup.addButton(btnMove)
	toolGroup.addButton(btnRotate)
	toolGroup.addButton(btnScale)
	toolGroup.addButton(btnRect)
	toolbar.addLeftWidget(toolGroup)

	handleGroup = ToolButtonGroup(False)
	btnHandle1 = ToggleableToolButton('tool_handle_pivot.png', 'tool_handle_center.png')
	btnHandle2 = ToggleableToolButton('tool_handle_global.png', 'tool_handle_local.png')
	handleGroup.addButton(btnHandle1)
	handleGroup.addButton(btnHandle2)
	btnSnap = CheckableToolButton('tool_snap.png')
	handleGroup.addButton(btnSnap)
	toolbar.addLeftWidget(handleGroup)

	# init center widgets
	btnPlay = CheckableToolButton('play.png')
	btnPause = CheckableToolButton('pause.png')
	btnStep = CheckableToolButton('step.png')
	btnStep.setEnabled(False)
	toolbar.addCenterWidget(btnPlay)
	toolbar.addCenterWidget(btnPause)
	toolbar.addCenterWidget(btnStep)
	return toolbar

def createToolBar(parent = None):
	toolbar = QToolBar('main', parent)
	toolbar.addWidget(_createToolBarImpl())
	toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
	toolbar.setFloatable(False)
	toolbar.setMovable(False)
	return toolbar
	