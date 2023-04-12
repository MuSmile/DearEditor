import os
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, QMimeData
from editor.common.util import getFileIcon, Qt_DecorationExpandedRole
from editor.common.icon_cache import getThemePixmap

class FileSystemItem:
	def __init__(self, path = None):
		self.parent = None
		self.children = []
		self.path = path
		self.datas = {}

	def data(self, role):
		if role == Qt.EditRole: return self.name()
		if role == Qt.DisplayRole: return self.name()
		if role == Qt.DecorationRole: return self.icon()
		if role == Qt_DecorationExpandedRole: return self.iconExpanded()
		if role in self.datas: return self.datas[ role ]

	def setData(self, data, role):
		if role == Qt.EditRole: return self.updateName(data)
		if role == Qt.DisplayRole: return self.updateName(data)
		if role == Qt.DecorationRole: return
		if role == Qt_DecorationExpandedRole: return
		self.datas[ role ] = data

	def name(self):
		if not self.path: return
		basename = os.path.basename(self.path)
		# return os.path.splitext(basename)[0]
		return basename

	def icon(self):
		if not self.path: return
		if os.path.isdir(self.path):
			return getThemePixmap('folder_close.png')
		else:
			return getFileIcon(self.path)

	def iconExpanded(self):
		if not self.path: return
		if os.path.isdir(self.path):
			if self.childCount() == 0: return
			return getThemePixmap('folder_opened.png')
		else:
			return getFileIcon(self.path)


	def updateName(self, name):
		# assert(self.path)
		# dirname = os.path.dirname(self.path)
		# os.path.join(dirname, name)
		pass

	def childCount(self):
		return len(self.children)

	def child(self, row):
		if 0 <= row and row < len(self.children):
			return self.children[row]

	def row(self):
		return self.parent.children.index(self) if self.parent else -1

	def appendChild(self, child):
		child.parent = self
		self.children.append(child)

	def insertChild(self, pos, child):
		child.parent = self
		self.children.insert(pos, child)

	def depth(self):
		p = self.parent
		depth = 0
		while p:
			depth += 1
			p = p.parent
		return depth


class FileSystemModel(QAbstractItemModel):
	MimeType = 'application/deardear-filesystemmodel'

	def __init__(self, keepFoldersOnTop = True, folderOnly = False, flat = False):
		super().__init__()
		self.invisibleRoot = FileSystemItem()
		self.keepFoldersOnTop = keepFoldersOnTop
		self.folderOnly = folderOnly
		self.flat = flat

	def acceptEntry(self, entry):
		if self.folderOnly and entry.is_file(): return False

		name = entry.name
		if name.startswith('.'): return False
		if name.endswith('~'): return False
		if name.startswith('__') and name.endswith('__'): return False
		return True

	def addRootItem(self, path):
		path = os.path.realpath(path)
		rootItem = FileSystemItem(path)
		self.invisibleRoot.appendChild(rootItem)

	def addRootItemsFrom(self, path):
		parent = self.invisibleRoot
		entries = [entry for entry in os.scandir(path) if self.acceptEntry(entry)]
		if self.keepFoldersOnTop:
			files, dirs = [], []
			for entry in entries:
				list = files if entry.is_file() else dirs
				list.append(entry)
			dirs.sort(key = lambda entry: entry.path)
			for d in dirs: parent.appendChild(FileSystemItem(d.path))
			files.sort(key = lambda entry: entry.path)
			for f in files: parent.appendChild(FileSystemItem(f.path))

		else:
			entries.sort(key = lambda entry: entry.path)
			for p in entries: parent.appendChild(FileSystemItem(p.path))

	def item(self, index):
		return index.internalPointer() if index and index.isValid() else self.invisibleRoot

	def rowCount(self, index):
		# return self.item(index).childCount()
		item = self.item(index)
		if item.childCount() > 0: return item.childCount()
		if not self.flat and os.path.isdir(item.path):
			entries = [entry for entry in os.scandir(item.path) if self.acceptEntry(entry)]
			return len(entries)
		else:
			return 0

	def columnCount(self, index):
		return 1

	def index(self, row, column = 0, parent = None):
		item = self.item(parent).child(row)
		return self.createIndex(row, column, item) if item else QModelIndex()

	def sibling(self, row, column, index):
		item = self.item(index)
		if not item.parent: return QModelIndex()
		if item.parent.childCount() <= row: return QModelIndex()
		siblingItem = item.parent.children[row]
		return self.createIndex(row, 0, siblingItem) if siblingItem else QModelIndex()
		
	def parent(self, index):
		item = self.item(index)
		parentItem = item.parent
		if not parentItem: return QModelIndex()
		return self.createIndex(parentItem.row(), 0, parentItem) if parentItem else QModelIndex()

	def data(self, index, role = Qt.DisplayRole):
		if not index or not index.isValid(): return
		return index.internalPointer().data(role)

	def setData(self, index, data, role = Qt.DisplayRole):
		if not index or not index.isValid(): return
		index.internalPointer().setData(data, role)
		self.dataChanged.emit(index, index, [role])

	def setDatas(self, indexes, data, role = Qt.DisplayRole):
		for idx in indexes: idx.internalPointer().setData(data, role)
		self.dataChanged.emit(indexes[0], indexes[-1], [ role ] * len(indexes))

	def flags(self, index):
		if not index or not index.isValid(): return Qt.NoItemFlags
		depth = index.internalPointer().depth()
		flags = Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
		if depth > 1: flags |= Qt.ItemIsEditable
		return flags

	def removeRows(self, row, count, parent):
		self.beginRemoveRows(parent, row, row + count)
		parentItem = self.item(parent)
		for i in range(count): parentItem.children.pop(row)
		self.endRemoveRows()
		return True

	def moveRows(self, srcParent, srcRow, count, dstParent, dstRow):
		super().moveRows(srcParent, srcRow, count, dstParent, dstRow)

	def insertRows(self, row, count, parent):
		self.beginInsertRows(parent, row, row + count)
		parentItem = self.item(parent)
		for i in range(count): parentItem.insertChild(row, FileSystemItem())
		self.endInsertRows()
		return True

	def supportedDragActions(self):
		return Qt.CopyAction | Qt.MoveAction

	def supportedDropActions(self):
		return Qt.CopyAction | Qt.MoveAction

	def canDropMimeData(self, mimeData, dropAction, row, column, parent):
		return (mimeData.hasFormat(self.MimeType)
			or mimeData.hasFormat('text/uri-list'))

	def mimeData(self, indexes):
		if not indexes: return None
		data = QMimeData()
		pathes = ','.join([idx.internalPointer().path for idx in indexes])
		data.setData(self.MimeType, bytes(pathes, 'utf-8'))
		return data

	def dropMimeData(self, mimeData, dropAction, row, column, parent):
		if not mimeData: return False
		if mimeData.hasFormat(self.MimeType):
			if self.canFetchMore(parent): self.fetchMore(parent)
			data = str(mimeData.data(self.MimeType), 'utf-8')
			for path in data.split(','):
				self.insertRows(row, 1, parent)
				idx = self.index(row, 0, parent)
				idx.internalPointer().path = path
		return True

	def canFetchMore(self, parent):
		if self.flat: return False
		parentItem = self.item(parent)
		if parentItem.childCount() > 0: return False
		path = parentItem.path
		if not os.path.isdir(path): return False
		for entry in os.scandir(path):
			if self.acceptEntry(entry):
				return True
		return False

	def fetchMore(self, parent):
		parentItem = parent.internalPointer()
		entries = [entry for entry in os.scandir(parentItem.path) if self.acceptEntry(entry)]
		# self.beginInsertRows(parent, 0, len(entries))

		if self.keepFoldersOnTop:
			files, dirs = [], []
			for entry in entries:
				list = files if entry.is_file() else dirs
				list.append(entry)
			dirs.sort(key = lambda entry: entry.path)
			for d in dirs: parentItem.appendChild(FileSystemItem(d.path))
			files.sort(key = lambda entry: entry.path)
			for f in files: parentItem.appendChild(FileSystemItem(f.path))

		else:
			entries.sort(key = lambda entry: entry.path)
			for p in entries: parentItem.appendChild(FileSystemItem(p.path))

		# self.endInsertRows()

	def reset(self):
		self.beginResetModel()
		self.invisibleRoot.children = []
		self.endResetModel()

