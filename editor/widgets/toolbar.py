from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QMenu, QToolBar, QToolButton, QPushButton, QButtonGroup, QHBoxLayout, QGridLayout, QSizePolicy
from editor.common.icon_cache import getThemeIcon

class _ToolButton(QToolButton):
	def __init__(self, icon, iconOn):
		super().__init__()
		self.icon = getThemeIcon(icon)
		self.iconOn = getThemeIcon(iconOn)

		self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(self.icon)
		self.toggled.connect(self.onButtonChecked)

	def onButtonChecked(self, checked):
		if checked:
			self.setIcon(self.iconOn)
		else:
			self.setIcon(self.icon)

class _TextToolButton(QPushButton):
	def __init__(self, text, icon, iconOn):
		super().__init__()
		self.icon = getThemeIcon(icon)
		self.iconOn = getThemeIcon(iconOn)

		self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(self.icon)
		self.setText(text)
		self.toggled.connect(self.onButtonChecked)

	def onButtonChecked(self, checked):
		if checked:
			self.setIcon(self.iconOn)
		else:
			self.setIcon(self.icon)

class _ToolToggle(QToolButton):
	def __init__(self, icon, iconOn):
		super().__init__()
		self.icon = getThemeIcon(icon)
		self.iconOn = getThemeIcon(iconOn)

		# self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(self.icon)
		self.checked = False
		self.clicked.connect(self.onButtonClicked)

	def onButtonClicked(self):
		self.checked = not self.checked
		if self.checked:
			self.setIcon(self.iconOn)
		else:
			self.setIcon(self.icon)

class _TextToolToggle(QPushButton):
	def __init__(self, text, textOn, icon, iconOn):
		super().__init__()
		self.icon = getThemeIcon(icon)
		self.iconOn = getThemeIcon(iconOn)
		self.text = text
		self.textOn = textOn

		# self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(self.icon)
		self.setText(self.text)
		self.checked = False
		self.clicked.connect(self.onButtonClicked)

	def onButtonClicked(self):
		self.checked = not self.checked
		if self.checked:
			self.setIcon(self.iconOn)
			self.setText(self.textOn)
		else:
			self.setIcon(self.icon)
			self.setText(self.text)

class _PopupToolButton(QPushButton):
	def __init__(self, text):
		super().__init__()

		self.setObjectName('popup')
		self.setFocusPolicy(Qt.NoFocus)
		self.setText(text)
		self.pressed.connect(self.showMenu)
		# self.setPopupMode(QToolButton.MenuButtonPopup)

	def addTestMenu(self):
		menu = QMenu(self)
		menu.setAttribute(Qt.WA_TranslucentBackground)
		menu.setWindowFlag(Qt.FramelessWindowHint, True)
		act1 = menu.addAction("New")
		menu.addSeparator()
		act2 = menu.addAction("Open")
		act2.setCheckable(True)
		act2.setChecked(True)
		act3 = menu.addAction("Quit")
		act4 = menu.addAction("Long item")
		if (self.text() == 'build'):
			act4.setShortcut('Meta+T')
			act4.triggered.connect(lambda: print('shit'))
			act4.setShortcutContext(Qt.ApplicationShortcut)
			act4.setShortcutVisibleInContextMenu(True)


		submenu = QMenu('test', menu)
		submenu.setAttribute(Qt.WA_TranslucentBackground)
		submenu.setWindowFlag(Qt.FramelessWindowHint, True)
		subact1 = submenu.addAction("New")
		submenu.addSeparator()
		menu.addMenu(submenu)
		submenu.addAction("test")

		self.setMenu(menu)


class _ToolButtonGroup(QWidget):
	def __init__(self, exclusive = True):
		super().__init__()
		self.group = QButtonGroup()
		self.group.setExclusive(exclusive)
		self.layout = QHBoxLayout()
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)

	def addButton(self, button):
		self.layout.addWidget(button)
		self.group.addButton(button)

class _ToolBarContainer(QWidget):
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
		self.containerL = _ToolBarContainer(Qt.AlignLeft  , 7)
		self.containerM = _ToolBarContainer(Qt.AlignCenter, 0)
		self.containerR = _ToolBarContainer(Qt.AlignRight , 5)
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

	# init right widgets
	btnBuild = _PopupToolButton('build')
	btnBuild.addTestMenu()
	btnLayer = _PopupToolButton('layer')
	btnLayer.addTestMenu()
	btnLayout = _PopupToolButton('layout')
	btnLayout.addTestMenu()

	toolbar.addRightWidget(btnBuild)
	toolbar.addRightWidget(btnLayer)
	toolbar.addRightWidget(btnLayout)

	# init left widgets
	btnViewMove = _ToolButton('tool_viewmove.png', 'tool_viewmove_on.png')
	btnMove = _ToolButton('tool_move.png', 'tool_move_on.png')
	btnRotate = _ToolButton('tool_rotate.png', 'tool_rotate_on.png')
	btnScale = _ToolButton('tool_scale.png', 'tool_scale_on.png')
	btnViewMove.setChecked(True)

	toolGroup = _ToolButtonGroup()
	toolGroup.addButton(btnViewMove)
	toolGroup.addButton(btnMove)
	toolGroup.addButton(btnRotate)
	toolGroup.addButton(btnScale)
	toolbar.addLeftWidget(toolGroup)

	handleGroup = _ToolButtonGroup(False)
	btnHandle1 = _ToolToggle('tool_handle_pivot.png', 'tool_handle_center.png')
	btnHandle2 = _ToolToggle('tool_handle_global.png', 'tool_handle_local.png')
	# btnHandle1 = _TextToolToggle('pivot ', 'center', 'tool_handle_pivot.png', 'tool_handle_center.png')
	# btnHandle2 = _TextToolToggle('global', 'local ', 'tool_handle_global.png', 'tool_handle_local.png')
	handleGroup.addButton(btnHandle1)
	handleGroup.addButton(btnHandle2)
	btnSnap = _ToolButton('tool_snap.png', 'tool_snap_on.png')
	handleGroup.addButton(btnSnap)
	toolbar.addLeftWidget(handleGroup)

	# init center widgets
	btnPlay = _ToolButton('play.png', 'play_on.png')
	btnPause = _ToolButton('pause.png', 'pause_on.png')
	btnStep = _ToolButton('step.png', 'step_on.png')
	btnStep.setEnabled(False)
	toolbar.addCenterWidget(btnPlay)
	toolbar.addCenterWidget(btnPause)
	toolbar.addCenterWidget(btnStep)
	return toolbar

def createMainToolBar(parent = None):
	toolbar = QToolBar('main', parent)
	toolbar.addWidget(_createToolBarImpl())
	toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
	toolbar.setFloatable(False)
	toolbar.setMovable(False)
	return toolbar
	