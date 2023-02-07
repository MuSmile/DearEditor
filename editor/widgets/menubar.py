from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar
from editor.tools.logger import warn

_typeItem, _typeGroup, _typeSeparator = range(3)

class MenuItem():
	def __init__(self, label, triggered, priority, shortcut = None, icon = None, checkable = False, checked = False):
		super().__init__()
		self.label     = label
		self.triggered = triggered
		self.priority  = priority
		self.icon      = icon
		self.shortcut  = shortcut
		self.checkable = checkable
		self.checked   = checked

		self.type = _typeItem
		self.widget = None

	def createWidget(self, parent = None):
		if not self.widget:
			action = QAction(self.label, parent)
			action.setAutoRepeat(False)
			if self.triggered: action.triggered.connect(self.triggered)
			if self.icon: action.setIcon(self.icon)
			if self.shortcut:
				action.setShortcut(self.shortcut)
				action.setShortcutContext(Qt.ApplicationShortcut)
			if self.checkable:
				action.setCheckable(True)
				action.setChecked(self.checked)
			self.widget = action
		return self.widget

class MenuItemGroup():
	def __init__(self, label, priority):
		super().__init__()
		self.label    = label
		self.priority = priority
		self.children = []

		self.type = _typeGroup
		self.widget = None

	def createWidget(self, parent = None):
		if not self.widget:
			menu = QMenu(self.label, parent)
			self.children.sort(key = lambda child: child.priority)
			prevLayer = None
			for child in self.children:
				layer = child.priority // 10
				if prevLayer and prevLayer < layer: menu.addSeparator()
				prevLayer = layer

				widget = child.createWidget(menu)
				if child.type == _typeGroup:
					menu.addMenu(widget)
				else:
					menu.addAction(widget)
			self.widget = menu
		return self.widget

class MenuItemSeparator():
	def __init__(self, priority):
		super().__init__()
		self.priority = priority
		self.type = _typeSeparator
		self.widget = None

	def createWidget(self, parent = None):
		if not self.widget:
			self.widget = QAction(parent)
			self.widget.setSeparator(True)
		return self.widget

class MenuTree():
	def __init__(self):
		super().__init__()
		self.rootMenus = []
		self.itemTable = {}
		self.menubar   = None

	def addItem(self, path, function, priority, shortcut = None, icon = None, checkable = False, checked = False):
		if self.menubar: return warn('menubar has created, skip modifying.')
		assert(path not in self.itemTable)
		
		idx = path.rfind('/')
		assert(idx > 0)

		name, pname = path[idx + 1:], path[:idx]
		item = MenuItem(name, function, priority, shortcut, icon, checkable, checked)
		group = self.affirmGroup(pname, priority)
		group.children.append(item)
		self.itemTable[path] = item

	def affirmGroup(self, path, priority):
		if self.menubar: return warn('menubar has created, skip modifying.')

		group = self.find(path)
		if group: return group

		idx = path.rfind('/')
		if idx > -1:
			name, pname = path[idx + 1:], path[:idx]
			group = MenuItemGroup(name, priority)
			pgroup = self.affirmGroup(pname, priority)
			pgroup.children.append(group)
			self.itemTable[path] = group
			return group

		else:
			group = MenuItemGroup(path, priority)
			self.rootMenus.append(group)
			self.itemTable[path] = group
			return group

	def insertSeparator(self, groupPath, priority):
		if self.menubar: return warn('menubar has created, skip modifying.')
		group = self.affirmGroup(groupPath, priority)
		separator = MenuItemSeparator(name, priority)
		group.children.append(separator)

	def find(self, path):
		if path in self.itemTable:
			return self.itemTable[path]
		else:
			return None

	def createMenuBar(self, parent = None):
		self.menubar = QMenuBar(parent)
		self.menubar.setContextMenuPolicy(Qt.PreventContextMenu)
		self.rootMenus.sort(key = lambda menu: menu.priority)
		for menu in self.rootMenus:
			widget = menu.createWidget(self.menubar)
			self.menubar.addMenu(widget)
		return self.menubar


##############    APIs    ##############
_menuTree = MenuTree()

def createMainMenuBar(parent = None):
	return _menuTree.createMenuBar(parent)

def registerMenuItem(path, func, priority, shortcut = None, icon = None, checkable = False, checked = False):
	_menuTree.addItem(path, func, priority, shortcut, icon, checkable, checked)

def registerMenuGroup(path, priority):
	_menuTree.affirmGroup(path, priority)

def registerMenuSeparator(groupPath, priority):
	_menuTree.insertSeparator(groupPath, priority)

def addMenuItem(path, priority, shortcut = None, icon = None, checkable = False, checked = False):
	def warpper(func):
		registerMenuItem(path, func, priority, shortcut, icon, checkable, checked)
		return func
	return warpper
