import sys, os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class FileSystemNode:
    def __init__(self, path):
        self.datas = {}
        self.children = []
        self.parent = None
        self.path = path

    def data(self, role):
        if role == Qt.EditRole: return self.name()
        if role == Qt.DisplayRole: return self.name()
        if role == Qt.DecorationRole: return self.icon()
        if role in self.datas: return self.datas[ role ]

    def setData(self, data, role):
        if role == Qt.EditRole: return
        if role == Qt.DisplayRole: return
        if role == Qt.DecorationRole: return
        self.datas[ role ] = data

    def name(self):
        return self.path
    def icon(self):
        base = os.environ[ 'DEAR_BASE_PATH' ]
        info = None
        if self.childCount() > 0:
            info = QFileInfo(base)
        else:
            info = QFileInfo(base + '/main.py')
        ip = QFileIconProvider()
        return ip.icon(info)

    def childCount(self):
        return len(self.children)

    def child(self, row):
        if row >= 0 and row < len(self.children):
            return self.children[row]

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        else:
            return -1

    def addChild(self, child):
        child.parent = self
        self.children.append(child)


class FileSystemModel(QAbstractItemModel):
    def __init__(self, root):
        super().__init__()
        self.root = FileSystemNode(root)
        # fetch sub folders
        # for node in nodes:
        #     self.root.addChild(node)
        assetsNode = FileSystemNode(root)
        self.root.addChild(assetsNode)
        for x in range(5):
            assetsNode.addChild(FileSystemNode(f'{root}/{x}'))

    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        else:
            return self.root.childCount()

    def columnCount(self, index):
        return 1

    def addChild(self, node, parent):
        if not parent or not parent.isValid():
            self.root.addChild(node)
        else:
            parent.internalPointer().addChild(node)

    def index(self, row, column, parent = None):
        pnode = None
        if not parent or not parent.isValid():
            pnode = self.root
        else:
            pnode = parent.internalPointer()

        if not QAbstractItemModel.hasIndex(self, row, column, parent):
            return QModelIndex()

        child = pnode.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent
            if p: return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()

    def data(self, index, role):
        if not index.isValid(): return
        return index.internalPointer().data(role)

    def setData(self, index, data, role):
        if not index.isValid(): return
        index.internalPointer().setData(data, role)
        self.dataChanged.emit(index, index, [role])

    def flags(self, index):
        # if not index.isValid(): return Qt.ItemIsSelectable | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEnabled

    def removeRows(self, row, count, parent):
        pnode = None
        self.beginRemoveRows(parent, row, row + count)
        if not parent.isValid():
            pnode = self.root
        else:
            pnode = parent.internalPointer()
        for i in range(count): pnode.children.pop(row)
        self.endRemoveRows()
        return True

    def insertRows(self, row, count, parent):
        pnode = None
        self.beginInsertRows(parent, row, row + count)
        if not parent.isValid():
            pnode = self.root
        else:
            pnode = parent.internalPointer()
        for i in range(count): pnode.children.insert(row, FileSystemNode(None))
        self.endInsertRows()
        return True

    def supportedDragActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def canDropMimeData(self, mimeData, dropAction, row, column, parent):
        return True

    def mimeData(self, indexes):
        return super().mimeData(indexes)

    def dropMimeData(self, mimeData, dropAction, row, column, parent):
        if not mimeData: return False
        print(mimeData.text())
        return True

    def canFetchMore(self, parent):
        return parent.isValid()

    def fetchMore(self, parent):
        pass
