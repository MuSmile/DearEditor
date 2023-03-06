from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QMenu, QToolBar, QToolButton, QPushButton, QButtonGroup, QHBoxLayout, QGridLayout, QSizePolicy
from editor.common.icon_cache import getThemeIcon

class CheckableToolButton(QToolButton):
	def __init__(self, icon):
		super().__init__()
		self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(getThemeIcon(icon))

class IconTextToolButton(QPushButton):
	def __init__(self, text, icon):
		super().__init__()

		self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(getThemeIcon(icon))
		self.setText(text)

class ToggleableToolButton(QToolButton):
	def __init__(self, icon1, icon2):
		super().__init__()
		self.icon1 = getThemeIcon(icon1)
		self.icon2 = getThemeIcon(icon2)

		# self.setCheckable(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.setIcon(self.icon1)
		self.checked = False
		self.clicked.connect(self.onButtonClicked)

	def onButtonClicked(self):
		self.checked = not self.checked
		if self.checked:
			self.setIcon(self.icon2)
		else:
			self.setIcon(self.icon1)

class PopupPushButton(QPushButton):
	def __init__(self, text):
		super().__init__()

		self.setObjectName('popup')
		self.setFocusPolicy(Qt.NoFocus)
		self.setText(text)
		# self.pressed.connect(self.showMenu)
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

class PopupToolButton(QToolButton):
	def __init__(self, text):
		super().__init__()

		self.setObjectName('popup')
		self.setFocusPolicy(Qt.NoFocus)
		self.setCheckable(True)
		self.setText(text)
		self.setPopupMode(QToolButton.MenuButtonPopup)

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
	btnSearch.setFixedWidth(20)

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
	