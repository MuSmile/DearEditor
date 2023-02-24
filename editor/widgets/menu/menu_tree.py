from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar
from editor.common.logger import warn


class MenuItem:
	def __init__(self, label, callback, shortcut, checkable, checked, priority, category):
		self.label     = label
		self.callback  = callback
		self.shortcut  = shortcut
		self.checkable = checkable
		self.checked   = checked
		self.priority  = priority
		self.category  = category

class MenuGroup:
	def __init__(self, label, priority):
		self.label    = label
		self.priority = priority
		self.children = []

	def find(self, label):
		for child in self.children:
			if child.label == label:
				return child

class MenuSeparator:
	def __init__(self, priority, category):
		self.priority = priority
		self.category = category


class MenuTree:
	def __init__(self, label = None):
		self.root = MenuGroup(label, None)
		self._maxPriority = None

	def _calcMaxPriority(self, group):
		maxPriority = float('-inf')
		for child in group.children:
			priority = self._calcMaxPriority(child) if isinstance(child, MenuGroup) else child.priority
			if priority > maxPriority: maxPriority = priority
		return maxPriority
	def _autoPriority(self):
		if self._maxPriority == None:
			return max(-1, self._calcMaxPriority(self.root)) + 1
		else:
			return self._maxPriority + 1


	#####################   API   #####################
	def addItem(self, path, callback, shortcut = None, checkable = False, checked = False, priority = None, category = None):
		if priority == None: priority = self._autoPriority()

		names = path.split('/')
		parent = self.root
		for name in names[:-1]:
			group = parent.find(name)
			if not group:
				group = MenuGroup(name, priority)
				parent.children.append(group)
			else:
				assert(isinstance(group, MenuGroup))
				if priority < group.priority: group.priority = priority

			parent = group

		name = names[-1]
		if parent.find(name): return warn(f'menu item with same name(\'{path}\') has registered, skip this.')
		item = MenuItem(name, callback, shortcut, checkable, checked, priority, category)
		parent.children.append(item)
		if self._maxPriority == None or priority > self._maxPriority: self._maxPriority = priority

	def addSeparator(self, groupPath, priority = None, category = None):
		if priority == None: priority = self._autoPriority()

		parent = self.root
		if groupPath:
			names = groupPath.split('/')
			for name in names:
				group = parent.find(name)
				if not group:
					group = MenuGroup(name, priority)
					parent.children.append(group)
				else:
					assert(isinstance(group, MenuGroup))
					if priority < group.priority: group.priority = priority

				parent = group

		separator = MenuSeparator(priority, category)
		parent.children.append(separator)
		if self._maxPriority == None or priority > self._maxPriority: self._maxPriority = priority

	def removeCategory(self, category, group = None):
		if group == None: group = self.root
		count = len(group.children)
		for i in range(count):
			idx = count - i - 1
			child = group.children[idx]
			if isinstance(child, MenuGroup):
				self.removeCategory(category, child)
				if len(child.children) == 0:
					del group.children[idx]
			else:
				if child.category == category:
					del group.children[idx]
		self._maxPriority = None

	def createWidget(self, parent):
		def _createItem(item, parent):
			action = QAction(item.label, parent)
			action.setAutoRepeat(False)
			if item.callback: action.callback.connect(item.callback)
			if item.shortcut:
				action.setShortcut(item.shortcut)
				action.setShortcutContext(Qt.ApplicationShortcut)
			if item.checkable:
				action.setCheckable(True)
				action.setChecked(item.checked)
			return action
		def _createSeparator(parent):
			action = QAction(parent)
			action.setSeparator(True)
			return action
		def _createGroup(group, parent):
			menu = QMenu(group.label, parent)
			group.children.sort(key = lambda child: child.priority)
			prevLayer = None
			for child in group.children:
				layer = child.priority // 100
				if prevLayer != None and prevLayer < layer: menu.addSeparator()
				prevLayer = layer

				if isinstance(child, MenuItem):
					menu.addAction(_createItem(child, parent))
				elif isinstance(child, MenuSeparator):
					menu.addAction(_createSeparator(parent))
				else:
					menu.addMenu(_createGroup(child, parent))
			return menu
		return _createGroup(self.root, parent)


	#####################  DEBUG  #####################
	def sort(self, group = None):
		if group == None: group = self.root
		group.children.sort(key = lambda child: child.priority)
		for child in group.children:
			if isinstance(child, MenuGroup):
				self.sort(child)
	def dumpItem(self, depth, item):
		indent = '    ' * depth
		name = '----' if isinstance(item, MenuSeparator) else item.label
		print('{:<24} : {}'.format(indent + name, item.priority))
		if isinstance(item, MenuGroup):
			for child in item.children:
				self.dumpItem(depth + 1, child)
	def dumpTree(self):
		for child in self.root.children:
			self.dumpItem(0, child)


if __name__ == '__main__':
	t = MenuTree('demo')
	t.addItem('foo', None, priority = None)
	t.addItem('bar', None, priority = 2, category = 'builtin')
	t.addItem('abar', None, priority = 100)
	t.addItem('test', None, priority = None)

	t.addItem('a/test', None, priority = 13)
	t.addItem('a/bar', None, priority = 11)
	t.addItem('a/foo', None, priority = 10)

	t.addItem('z/b/test', None, priority = 22)
	t.addItem('z/c/bar', None, priority = 21)
	t.addItem('z/c/foo', None, priority = 20)

	t.addSeparator(None, priority = 12)
	t.addItem('a', None, priority = 9)

	t.addItem('a/b/test', None, priority = 22)
	t.addItem('a/c/bar', None, priority = 21)
	t.addItem('a/c/foo', None, priority = 20)

	t.sort()
	t.removeCategory(None)
	t.addItem('a', None)
	t.dumpTree()

