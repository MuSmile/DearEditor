import os
from enum import Enum
from PySide6.QtCore import Qt, QItemSelectionModel, QModelIndex, QMimeData
from PySide6.QtGui import QStandardItem
from editor.models.basic_model import BasicModel, Qt_DecorationExpandedRole, modelIndexDepth
from editor.common.icon_cache import getThemePixmap
from editor.common.util import getFileIcon


class ItemType(Enum):
	Normal         = 0
	Separator      = 1
	FavoriteRoot   = 2
	FavoriteSearch = 3
	FavoriteFolder = 4


_ItemTypeRole = Qt.UserRole + 98
_ItemDataRole = Qt.UserRole + 99

class AssetItem(QStandardItem):
	def __init__(self, type, data = None):
		super().__init__()
		self.setItemType(type)
		self.setItemData(data)

		if type == ItemType.Normal:
			assert(data)
			if os.path.isdir(data):
				self.setData(getThemePixmap('folder_close.png'), Qt.DecorationRole)
				self.setData(getThemePixmap('folder_opened.png'), Qt_DecorationExpandedRole)
			else:
				self.setData(getFileIcon(data), Qt.DecorationRole)
		elif type == ItemType.FavoriteRoot:
			self.setData(getThemePixmap('favorite.png'), Qt.DecorationRole)
		elif type == ItemType.FavoriteSearch:
			self.setData(getThemePixmap('search.png'), Qt.DecorationRole)
		elif type == ItemType.FavoriteFolder:
			self.setData(getThemePixmap('folder_close.png'), Qt.DecorationRole)

	def itemType(self):
		return super().data(_ItemTypeRole)
	def setItemType(self, type):
		super().setData(type, _ItemTypeRole)

	def itemData(self):
		return super().data(_ItemDataRole)
	def setItemData(self, data):
		if data: super().setData(data, _ItemDataRole)

	def clone(self):
		return AssetItem(self)

	def data(self, role):
		if role == Qt.EditRole: return self.itemName()
		if role == Qt.DisplayRole: return self.itemName()
		return super().data(role)

	def setData(self, data, role):
		if role == Qt.EditRole: return self.updateItemName(data)
		if role == Qt.DisplayRole: return self.updateItemName(data)
		super().setData(data, role)

	def updateItemName(self, name):
		itemType = self.itemType()
		if itemType == ItemType.Normal:
			data = self.itemData()
			assert(data)
			dirname = os.path.dirname(data)
			self.setItemData(os.path.join(dirname, name))
		elif itemType == ItemType.FavoriteSearch:
			self.setItemData(name)
		elif itemType == ItemType.FavoriteFolder:
			self.setItemData(name)

	def itemName(self):
		data = self.itemData()
		if not data: return
		if self.itemType() == ItemType.Normal:
			return os.path.basename(data)
		else:
			return data

class AssetModel(BasicModel):
	def __init__(self, folderOnly = True):
		super().__init__()
		self.folderOnly = folderOnly
		self.addFavoriteItem()
		self.addSeparatorItem()
		self.setItemPrototype(self.favoriteItem)

	def flags(self, index):
		if not index or not index.isValid(): return Qt.NoItemFlags

		itemType = self.itemFromIndex(index).itemType()
		if itemType == ItemType.Separator: return Qt.NoItemFlags
		if itemType == ItemType.FavoriteRoot: return Qt.ItemIsSelectable | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
		if itemType == ItemType.FavoriteSearch: return Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable
		if itemType == ItemType.FavoriteFolder: return Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable
		
		flags = Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
		if modelIndexDepth(index) > 0: flags |= Qt.ItemIsEditable
		return flags

	def acceptEntry(self, entry):
		if self.folderOnly and entry.is_file(): return False

		name = entry.name
		if name.startswith('.'): return False
		if name.endswith('~'): return False
		if name.startswith('__') and name.endswith('__'): return False
		return True

	def addFavoriteItem(self):
		self.favoriteItem = AssetItem(ItemType.FavoriteRoot, 'Favorites')
		materials = AssetItem(ItemType.FavoriteSearch, 'All Materials')
		prefabs = AssetItem(ItemType.FavoriteSearch, 'All Prefabs')
		scenes = AssetItem(ItemType.FavoriteSearch, 'All Scenes')

		self.favoriteItem.appendRow(materials)
		self.favoriteItem.appendRow(prefabs)
		self.favoriteItem.appendRow(scenes)
		self.appendRow(self.favoriteItem)

	def addSeparatorItem(self):
		self.blankItem = AssetItem(ItemType.Separator)
		self.blankItem.setData(12, Qt.SizeHintRole)
		self.appendRow(self.blankItem)

	def addPath(self, path):
		path = os.path.realpath(path)
		self.appendRow(self.affirmItem(path))

	def affirmItem(self, path):
		item = AssetItem(ItemType.Normal, path)
		entries = [entry for entry in os.scandir(path) if self.acceptEntry(entry)]
		if self.folderOnly:
			entries.sort(key = lambda entry: entry.path)
			for sub in entries: item.appendRow(self.affirmItem(sub.path))
		else:
			files, dirs = [], []
			for entry in entries:
				list = files if entry.is_file() else dirs
				list.append(entry)
			dirs.sort(key = lambda entry: entry.path)
			for d in dirs: item.appendRow(self.affirmItem(d.path))
			files.sort(key = lambda entry: entry.path)
			for f in files: item.appendRow(AssetItem(ItemType.Normal, f.path))
		return item

class FolderModel(BasicModel):
	def __init__(self, keepFoldersOnTop = True):
		super().__init__()
		self.keepFoldersOnTop = keepFoldersOnTop

	def flags(self, index):
		return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled

	def acceptEntry(self, entry):
		name = entry.name
		if name.startswith('.'): return False
		if name.endswith('~'): return False
		if name.startswith('__') and name.endswith('__'): return False
		return True

	def setFolder(self, path):
		self.clear()
		entries = [entry for entry in os.scandir(path) if self.acceptEntry(entry)]
		if self.keepFoldersOnTop:
			files, dirs = [], []
			for entry in entries:
				list = files if entry.is_file() else dirs
				list.append(entry)
			dirs.sort(key = lambda entry: entry.path)
			for d in dirs: self.appendRow(AssetItem(ItemType.Normal, d.path))
			files.sort(key = lambda entry: entry.path)
			for f in files: self.appendRow(AssetItem(ItemType.Normal, f.path))

		else:
			entries.sort(key = lambda entry: entry.path)
			for p in entries: self.appendRow(AssetItem(ItemType.Normal, p.path))
