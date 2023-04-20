from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QMenu, QToolBar, QToolButton, QPushButton, QButtonGroup, QHBoxLayout, QGridLayout, QSizePolicy
from editor.widgets.basic.button import ToggleToolButton, ButtonGroup
from editor.common.icon_cache import getThemeIcon

def checkableButton(icon, parent = None):
	btn = QToolButton(parent)
	btn.setCheckable(True)
	btn.setFocusPolicy(Qt.NoFocus)
	btn.setIcon(getThemeIcon(icon))
	return btn

def popupButton(text, parent = None):
	btn = QPushButton(parent)
	btn.setFocusPolicy(Qt.NoFocus)
	btn.setText(text)

	menu = QMenu(btn)
	act1 = menu.addAction("New")
	act1.setShortcut('Meta+Ctrl+Alt+Shift+Tab')
	act1.setShortcutVisibleInContextMenu(True)
	menu.addSeparator()
	act2 = menu.addAction("Open")
	act2.setCheckable(True)
	act2.setChecked(True)
	act3 = menu.addAction("Quit")
	act4 = menu.addAction("Long item")
	if text == 'Layout':
		act4.setShortcut('Ctrl+N')
		act4.triggered.connect(lambda: print('shit'))
		act4.setShortcutContext(Qt.ApplicationShortcut)
		act4.setShortcutVisibleInContextMenu(True)
	submenu = QMenu('test', menu)
	subact1 = submenu.addAction("New")
	submenu.addSeparator()
	menu.addMenu(submenu)
	submenu.addAction("test")

	btn.setMenu(menu)
	return btn

class MainToolBar(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		
		self.areaL = self.createAreaLayout(7)
		self.areaM = self.createAreaLayout(1)
		self.areaR = self.createAreaLayout(7)

		grid = QGridLayout(self)
		grid.addLayout(self.areaL, 0, 0, 1, 3, Qt.AlignLeft)
		grid.addLayout(self.areaM, 0, 3, 1, 1, Qt.AlignCenter)
		grid.addLayout(self.areaR, 0, 4, 1, 3, Qt.AlignRight)
		grid.setContentsMargins(0, 0, 0, 0)
		grid.setSpacing(10)

		self.initContents()

	def createAreaLayout(self, spacing):
		layout = QHBoxLayout()
		layout.setSpacing(spacing)
		layout.setContentsMargins(0, 0, 0, 0)
		return layout

	def addLeftWidget(self, widget): self.areaL.addWidget(widget)
	def addRightWidget(self, widget): self.areaR.addWidget(widget)
	def addCenterWidget(self, widget): self.areaM.addWidget(widget)

	def addLeftLayout(self, layout): self.areaL.addLayout(layout)
	def addRightLayout(self, layout): self.areaR.addLayout(layout)
	def addCenterLayout(self, layout): self.areaM.addLayout(layout)

	def initContents(self):
		btnSearch = QToolButton()
		btnSearch.setIcon(getThemeIcon('search.png'))
		btnSearch.setFixedWidth(22)

		btnBuild = QPushButton('Build')
		btnBuild.setIcon(getThemeIcon('build.png'))
		btnBuild.setFocusPolicy(Qt.NoFocus)
		btnLayer = popupButton('Layer')
		btnLayout = popupButton('Layout')

		self.addRightWidget(btnBuild)
		self.addRightWidget(btnLayer)
		self.addRightWidget(btnLayout)
		self.addRightWidget(btnSearch)

		# init left widgets
		btnViewMove = checkableButton('tool_viewmove.png')
		btnMove = checkableButton('tool_move.png')
		btnRotate = checkableButton('tool_rotate.png')
		btnScale = checkableButton('tool_scale.png')
		btnRect = checkableButton('tool_rect.png')
		btnViewMove.setChecked(True)

		toolGroup = ButtonGroup()
		toolGroup.layout().setSpacing(1)
		toolGroup.initFromButtons([btnViewMove, btnMove, btnRotate, btnScale, btnRect])
		self.addLeftWidget(toolGroup)

		handleLayout = QHBoxLayout()
		handleLayout.setSpacing(1)
		handleLayout.setContentsMargins(0, 0, 0, 0)
		btnHandle1 = ToggleToolButton('tool_handle_pivot.png', 'tool_handle_center.png')
		btnHandle2 = ToggleToolButton('tool_handle_global.png', 'tool_handle_local.png')
		handleLayout.addWidget(btnHandle1)
		handleLayout.addWidget(btnHandle2)
		btnSnap = checkableButton('tool_snap.png')
		handleLayout.addWidget(btnSnap)
		self.addLeftLayout(handleLayout)

		# init center widgets
		btnPlay = checkableButton('play.png')
		btnPause = checkableButton('pause.png')
		btnStep = checkableButton('step.png')
		btnPlay.setObjectName('center')
		btnPause.setObjectName('center')
		btnStep.setObjectName('center')
		btnStep.setEnabled(False)
		self.addCenterWidget(btnPlay)
		self.addCenterWidget(btnPause)
		self.addCenterWidget(btnStep)

def createToolBar(parent = None):
	toolbar = QToolBar('main', parent)
	toolbar.addWidget(MainToolBar(toolbar))
	toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
	toolbar.setFloatable(False)
	toolbar.setMovable(False)
	return toolbar
	