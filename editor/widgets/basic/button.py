from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QToolButton, QPushButton, QButtonGroup, QMenu, QStyleOptionToolButton, QStyle, QHBoxLayout
from editor.common.icon_cache import getThemeIcon

class ToggleToolButton(QToolButton):
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

class MenuPopupToolButton(QToolButton):
	def __init__(self, parent = None):
		super().__init__(parent)

		self.setFocusPolicy(Qt.NoFocus)
		self.setCheckable(True)

		self.menuBtn = QToolButton(self)
		self.menuBtn.clicked.connect(self.showPopupMenu)
		# self.menuBtn.clicked.connect(self.showMenu)
		
		self.addTestMenu()

	def showPopupMenu(self):
		pos = self.rect().bottomLeft()
		pos.setY(pos.y() + 1)
		self.menu().popup(self.mapToGlobal(pos))

	def resizeEvent(self, evt):
		option = QStyleOptionToolButton()
		self.initStyleOption(option)
		proxy = self.style().proxy()
		cc, sc = QStyle.CC_ToolButton, QStyle.SC_ToolButtonMenu
		self.menuBtn.setGeometry(proxy.subControlRect(cc, option, sc, self))

	def addTestMenu(self):
		menu = QMenu(self)
		act1 = menu.addAction("New")
		menu.addSeparator()
		act2 = menu.addAction("Open")
		act2.setCheckable(True)
		act2.setChecked(True)
		act3 = menu.addAction("Quit")

		submenu = QMenu('test', menu)
		subact1 = submenu.addAction("New")
		submenu.addSeparator()
		menu.addMenu(submenu)
		submenu.addAction("test")
		self.setMenu(menu)

class ButtonGroup(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)
		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

	def button(self, idx):
		return self.group.button(idx)

	def select(self, idx):
		btn = self.group.button(idx)
		btn.setChecked(True)

	def initFromItems(self, items):
		count = len(items)
		layout = self.layout()
		for i in range(count):
			btn = QPushButton(items[i])
			btn.setCheckable(True)
			layout.addWidget(btn)
			self.group.addButton(btn, i)
			if i == 0: btn.setObjectName('left')
			elif i == count - 1: btn.setObjectName('right')
			else: btn.setObjectName('middle')

	def initFromButtons(self, buttons):
		count = len(buttons)
		layout = self.layout()
		for i in range(count):
			btn = buttons[i]
			btn.setCheckable(True)
			layout.addWidget(btn)
			self.group.addButton(btn, i)
			if i == 0: btn.setObjectName('left')
			elif i == count - 1: btn.setObjectName('right')
			else: btn.setObjectName('middle')
