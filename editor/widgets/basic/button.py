from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton, QPushButton, QMenu
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

		# self.setCheckable(True)
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
		if (self.text() == 'Layout'):
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
