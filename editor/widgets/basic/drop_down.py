from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QMenu
from editor.common.icon_cache import getThemeIcon

class DropDown(QPushButton):
	def __init__(self, text):
		super().__init__()

		self.setObjectName('popup')
		self.setFocusPolicy(Qt.NoFocus)
		self.setText(text)
		# self.pressed.connect(self.showMenu)
		# self.setPopupMode(QToolButton.MenuButtonPopup)

	def addTestMenu(self):
		menu = QMenu(self)
		act1 = menu.addAction("New")
		act1.setShortcut('Meta+Ctrl+Alt+Shift+Tab')
		act1.setShortcutVisibleInContextMenu(True)
		menu.addSeparator()
		act2 = menu.addAction("Open")
		act2.setCheckable(True)
		act2.setChecked(True)
		act3 = menu.addAction("Quit")
		act4 = menu.addAction("Long item")
		if (self.text() == 'Layout'):
			act4.setShortcut('Ctrl+N')
			act4.triggered.connect(lambda: print('shit'))
			act4.setShortcutContext(Qt.ApplicationShortcut)
			act4.setShortcutVisibleInContextMenu(True)


		submenu = QMenu('test', menu)
		subact1 = submenu.addAction("New")
		submenu.addSeparator()
		menu.addMenu(submenu)
		submenu.addAction("test")

		self.setMenu(menu)
