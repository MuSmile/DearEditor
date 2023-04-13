import functools
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QApplication
from editor.common.icon_cache import getThemePixmap


#############################################
Qt_DecorationExpandedRole = Qt.UserRole + Qt.DecorationRole # Qt.UserRole + 1
'''Qt.ItemDataRole: User role for provide item expanded icon.
'''
Qt_AlternateRole = Qt.UserRole + 2
'''Qt.ItemDataRole: User role for indicate whether item use alternate background or not.
'''

#############################################
def modelIndexDepth(index):
	"""Calculate depth of a QModelIndex.
	
	Args:
		QModelIndex index: Given index to calculate.

	Returns:
		int: depth of given QModelIndex.
	"""
	depth = 0
	parent = index.parent()
	while parent.isValid():
		depth += 1
		parent = parent.parent()
	return depth

def modelIndexRowSequence(index):
	"""Calculate row number sequence of a QModelIndex.
	
	Args:
		QModelIndex index: Given index to calculate.

	Returns:
		list[int]: number sequence of given QModelIndex.
	"""
	seq = []
	curr = index
	while curr.isValid():
		seq.insert(0, curr.row())
		curr = curr.parent()
	return seq

def isAboveOfModelIndex(test, index):
	"""Check a given QModelIndex is above of another in model.
	
	Args:
		QModelIndex test: Given QModelIndex to check.
		QModelIndex index: Given QModelIndex to check against.

	Returns:
		bool: Weather given QModelIndex is above of another or not.
	"""
	seq1 = modelIndexRowSequence(test)
	seq2 = modelIndexRowSequence(index)
	len1 = len(seq1)
	len2 = len(seq2)
	for i in range(min(len1, len2)):
		row1 = seq1[i]
		row2 = seq2[i]
		if row1 < row2: return True
		if row1 > row2: return False
	return len1 < len2

def isChildOfModelIndex(test, index):
	"""Check a given QModelIndex is child of another.
	
	Args:
		QModelIndex test: Given QModelIndex to check.
		QModelIndex index: Given QModelIndex to check against.

	Returns:
		bool: Weather given QModelIndex is child of another or not.
	"""
	p = test.parent()
	while p.isValid():
		if p == index: return True
		p = p.parent()
	return False


#############################################
class BasicModel(QStandardItemModel):
	def __init__(self):
		super().__init__()
		# self.cutIndexes = None

	def flags(self, index):
		return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled

	def setDatas(self, indexes, data, role = Qt.DisplayRole):
		self.blockSignals(True)
		for idx in indexes: self.setData(idx, data, role)
		self.blockSignals(False)
		self.dataChanged.emit(indexes[0], indexes[-1], [ role ] * len(indexes))

	def moveSelections(self, view, dstParent, dstRow):
		selectionModel = view.selectionModel()
		srcIndexes = selectionModel.selectedIndexes()
		srcIndexes.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and 1 or -1))
		selectionModel.clear()

		delayRemoves = []
		for idx in srcIndexes:
			parent, row = idx.parent(), idx.row()
			if parent == dstParent and row < dstRow:
				delayRemoves.append(idx)
			elif parent == dstParent.parent() and row < dstParent.row():
				delayRemoves.append(idx)

		for idx in srcIndexes:
			mimeData = self.mimeData([idx])
			if idx not in delayRemoves: self.removeRow(idx.row(), idx.parent())
			self.dropMimeData(mimeData, Qt.CopyAction, dstRow, -1, dstParent)

		count = len(srcIndexes)
		view.setCurrentIndex(self.index(dstRow + count - 1, 0, dstParent))
		for i in range(dstRow, dstRow + count): selectionModel.select(self.index(i, 0, dstParent), QItemSelectionModel.Select)
		
		view.expandInstant(dstParent, False)
		for idx in delayRemoves: self.removeRow(idx.row(), idx.parent())

	def cutSelections(self, view):
		pass

	def copySelections(self, view):
		selectionModel = view.selectionModel()
		selections = selectionModel.selectedIndexes()
		selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and -1 or 1))

		# detect children and remove
		for i in range(len(selections) - 1, 0, -1):
			curr = selections[i]
			for j in range(i - 1, -1, -1):
				test = selections[j]
				if isChildOfModelIndex(curr, test):
					del selections[i]
					break

		clipboard = QApplication.clipboard()
		clipboard.setMimeData(self.mimeData(selections))

	def pasteSelections(self, view):
		selectionModel = view.selectionModel()
		toSelections = []
		parent = view.currentIndex().parent()
		clipboard = QApplication.clipboard()
		oldRowCount = self.rowCount(parent)
		self.dropMimeData(clipboard.mimeData(), Qt.CopyAction, -1, -1, parent)
		newRowCount = self.rowCount(parent)
		dropedCount = newRowCount - oldRowCount
		if dropedCount > 0:
			selectionModel.clear()
			
			view.setCurrentIndex(self.index(newRowCount - 1, 0, parent))
			for i in range(newRowCount - dropedCount, newRowCount):
				selection = self.index(i, 0, parent)
				selectionModel.select(selection, QItemSelectionModel.Select)

			while parent.isValid():
				view.expandInstant(parent, False)
				parent = parent.parent()

	def duplicateSelections(self, view):
		selectionModel = view.selectionModel()
		selections = selectionModel.selectedIndexes()
		selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and -1 or 1))
		
		# detect children and remove
		for i in range(len(selections) - 1, 0, -1):
			curr = selections[i]
			for j in range(i - 1, -1, -1):
				test = selections[j]
				if isChildOfModelIndex(curr, test):
					del selections[i]
					break

		selectionModel.clear()
		toSelections = []
		for selection in selections:
			parent = selection.parent()
			mimeData = self.mimeData([selection])
			self.dropMimeData(mimeData, Qt.CopyAction, -1, -1, parent)

			row = self.rowCount(parent) - 1
			toSelections.append(self.index(row, 0, parent))

			while parent.isValid():
				view.expandInstant(parent, False)
				parent = parent.parent()

		view.setCurrentIndex(toSelections[-1])
		for selection in toSelections:
			selectionModel.select(selection, QItemSelectionModel.Select)

