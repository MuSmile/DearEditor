from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar
from editor.common.logger import warn


class MenuItem:
	def __init__  (self, data): self.data = data
	def label           (self): return self.data['label'          ]
	def callback        (self): return self.data['callback'       ] if 'callback'        in self.data else None
	def shortcut        (self): return self.data['shortcut'       ] if 'shortcut'        in self.data else None
	def shortcutContext (self): return self.data['shortcutContext'] if 'shortcutContext' in self.data else None
	def checkable       (self): return self.data['checkable'      ] if 'checkable'       in self.data else False
	def checked         (self): return self.data['checked'        ] if 'checked'         in self.data else False
	def enabled         (self): return self.data['enabled'        ] if 'enabled'         in self.data else False
	def menuRole        (self): return self.data['menuRole'       ] if 'menuRole'        in self.data else None
	def priority        (self): return self.data['priority'       ] if 'priority'        in self.data else None
	def category        (self): return self.data['category'       ] if 'category'        in self.data else 'built-in'

	def createAction(self, parent):
		action = QAction(self.label(), parent)
		action.setAutoRepeat(False)
		if 'callback' in self.data:
			action.triggered.connect(self.data['callback'])
		if 'shortcut' in self.data:
			action.setShortcut(self.data['shortcut'])
			if 'shortcutContext' in self.data: action.setShortcutContext(self.data['shortcutContext'])
		if 'checkable' in self.data:
			action.setCheckable(self.data['checkable'])
			action.setChecked(self.checked())
		if 'enabled' in self.data:
			action.setEnabled(self.data['enabled'])
		if 'menuRole' in self.data:
			action.setMenuRole(self.data['menuRole'])
		return action

class MenuSeparator:
	def __init__ (self, data): self.data = data
	def priority (self): return self.data['priority' ] if 'priority'  in self.data else None
	def category (self): return self.data['category' ] if 'category'  in self.data else 'built-in'

	def createAction(self, parent):
		action = QAction(parent)
		action.setSeparator(True)
		return action

class MenuGroup:
	def __init__(self, data):
		self.data = data
		self.children = []

	def label    (self): return self.data['label'    ]
	def priority (self): return self.data['priority' ] if 'priority'  in self.data else None

	def find(self, label):
		for child in self.children:
			if isinstance(child, MenuSeparator): continue
			if child.label() == label: return child

	def createMenu(self, parent):
		menu = QMenu(self.label(), parent)
		self.children.sort(key = lambda child: child.priority())
		
		prevLayer = None
		for child in self.children:
			layer = child.priority() // 100
			if prevLayer != None and prevLayer < layer: menu.addSeparator()
			prevLayer = layer

			if isinstance(child, MenuGroup):
				menu.addMenu(child.createMenu(parent))
			else:
				menu.addAction(child.createAction(parent))
		return menu

class MenuTree:
	def __init__(self, label = None):
		self.root = MenuGroup( {'label' : label} )
		self._currMaxPriority = None

	def _calcCurrMaxPriority(self, group):
		maxPriority = float('-inf')
		for child in group.children:
			priority = self._calcCurrMaxPriority(child) if isinstance(child, MenuGroup) else child.priority()
			if priority > maxPriority: maxPriority = priority
		return maxPriority
	def _autoPriority(self):
		if self._currMaxPriority == None:
			return max(-1, self._calcCurrMaxPriority(self.root)) + 1
		else:
			return self._currMaxPriority + 1


	#####################   API   #####################
	def addItem(self, path, callback, shortcut = None, priority = None, **data):
		if priority == None: priority = self._autoPriority()

		names = path.split('/')
		parent = self.root
		for name in names[:-1]:
			group = parent.find(name)
			if not group:
				group = MenuGroup({
					'label'   : name,
					'priority': priority,
				})
				parent.children.append(group)
			else:
				assert(isinstance(group, MenuGroup))
				if priority < group.priority(): group.data['priority'] = priority

			parent = group

		name = names[-1]
		if parent.find(name): return warn(f'menu item with same name \'{path}\' has registered, skip this.')
		
		data['label'   ] = name
		data['priority'] = priority
		if callback: data['callback'] = callback
		if shortcut: data['shortcut'] = shortcut
		item = MenuItem(data)
		parent.children.append(item)
		if self._currMaxPriority == None or priority > self._currMaxPriority: self._currMaxPriority = priority

	def addSeparator(self, groupPath, priority = None, **data):
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
					if priority < group.priority(): group.data['priority'] = priority

				parent = group

		data['priority'] = priority
		separator = MenuSeparator(data)
		parent.children.append(separator)
		if self._currMaxPriority == None or priority > self._currMaxPriority: self._currMaxPriority = priority

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
				if child.category() == category:
					del group.children[idx]
		self._currMaxPriority = None

	def createWidget(self, parent):
		return self.root.createMenu(parent)


	#####################  DEBUG  #####################
	def sort(self, group = None):
		if group == None: group = self.root
		group.children.sort(key = lambda child: child.priority())
		for child in group.children:
			if isinstance(child, MenuGroup):
				self.sort(child)
	def dumpItem(self, depth, item):
		indent = '    ' * depth
		name = '----' if isinstance(item, MenuSeparator) else item.label
		print('{:<24} : {}'.format(indent + name, item.priority()))
		if isinstance(item, MenuGroup):
			for child in item.children:
				self.dumpItem(depth + 1, child)
	def dumpTree(self):
		for child in self.root.children:
			self.dumpItem(0, child)


#####################  TEST  #####################
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

