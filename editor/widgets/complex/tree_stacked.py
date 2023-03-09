from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QStackedWidget, QSplitter, QScrollArea, QWidget
from PySide6.QtGui import QStandardItem, QStandardItemModel
from editor.widgets.complex.tree_view import TreeView

class TreeStackedWidget(QSplitter):
	def __init__(self, parent):
		super().__init__(parent)
		self.itemIndexTable = {}

		self.tree = self.createTreeView()
		self.stacked = self.createStackedView()
		self.addWidget(self.tree)
		self.addWidget(self.stacked)

		self.setOrientation(Qt.Horizontal)
		self.setChildrenCollapsible(False)
		self.setSizes([100, 300])

	def eventFilter(self, obj, evt):
		if obj == self.tree and evt.type() == QEvent.KeyPress:
			key = evt.key()
			if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_Up or key == Qt.Key_Down:
				self.tree.keyPressEvent(evt)
			return True
		return False

	def createTreeView(self):
		tree = TreeView(self)
		tree.setModel(QStandardItemModel())
		tree.selectionModel().currentChanged.connect(self.onCurrentChanged)
		tree.installEventFilter(self)
		return tree

	def createStackedView(self):
		stacked = QStackedWidget(self)
		stacked.addWidget(self.createStackedEmpty())
		stacked.setCurrentIndex(0)
		return stacked

	def createStackedEmpty(self):
		empty = QWidget()
		empty.setObjectName('empty')
		return empty

	def affirmTabItem(self, name, parent):
		for i in range(parent.rowCount()):
			child = parent.child(i)
			if child.text() == name:
				return child
		newItem = QStandardItem(name)
		parent.appendRow(newItem)
		return newItem

	def addStackedWidget(self, path, widget):
		model = self.tree.model()
		curr = model.invisibleRootItem()
		for name in path.split('/'): curr = self.affirmTabItem(name, curr)

		area = QScrollArea(self)
		area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		area.setWidgetResizable(True)
		area.setWidget(widget)
		idx = self.stacked.addWidget(area)
		self.itemIndexTable[ path ] = idx

	def setCurrentPath(self, path):
		if path not in self.itemIndexTable:
			self.stacked.setCurrentIndex(0)
		else:
			self.stacked.setCurrentIndex(self.itemIndexTable[ path ])

	def onCurrentChanged(self, curr, prev):
		if curr == prev: return
		if not curr.isValid():
			self.stacked.setCurrentIndex(0)
		else:
			self.setCurrentPath(self.path(curr))

	def path(self, index):
		path = index.data()
		parent = index.parent()
		if parent.isValid(): path = self.path(parent) + '/' + path
		return path
