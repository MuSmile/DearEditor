import math
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtWidgets import QLayout

class FlowLayout(QLayout):
	def __init__(self, parent = None):
		super().__init__(parent)
		self._spacings = (0, 0)
		self._itemList = []
		self._itemSize = None

	def __del__(self):
		self._itemList.clear()

	def setContentsSpacings(self, horizontal, vertical):
		self._spacings = (horizontal, vertical)

	def setFixedItemSize(self, size):
		for item in self._itemList: item.widget().setFixedSize(size, size)
		self._itemSize = size

	def addItem(self, item):
		if self._itemSize != None: item.widget().setFixedSize(self._itemSize, self._itemSize)
		self._itemList.append(item)

	def count(self):
		return len(self._itemList)

	def itemAt(self, index):
		if index < 0: return None
		if index >= len(self._itemList): return None
		return self._itemList[index]

	def takeAt(self, index):
		if index < 0: return None
		if index >= len(self._itemList): return None
		return self._itemList.pop(index)

	def expandingDirections(self):
		return Qt.Orientations(Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		ml, mt, mr, mb = self.getContentsMargins()
		x, y, h = ml, mt, 0

		for item in self._itemList:
			sizeHint = item.sizeHint()
			itemW, itemH = sizeHint.width(), sizeHint.height()
			spaceX, spaceY = self._spacings

			nextX = x + itemW + spaceX
			if nextX - spaceX + mr > width and h > 0:
				x, y, h = ml, y + h + spaceY, 0
				nextX = x + itemW + spaceX

			x, h = nextX, max(h, itemH)

		return y + h + mb

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QSize()
		for item in self._itemList: size = size.expandedTo(item.minimumSize())
		ml, mt, mr, mb = self.getContentsMargins()
		size += QSize(ml + mr, mt + mb)
		return size

	def setGeometry(self, rect):
		super().setGeometry(rect)
		self.doLayout(rect)

	def doLayout(self, rect):
		ml, mt, mr, mb = self.getContentsMargins()
		x, y, h = rect.x() + ml, rect.y() + mt, 0

		for item in self._itemList:
			sizeHint = item.sizeHint()
			itemW, itemH = sizeHint.width(), sizeHint.height()
			spaceX, spaceY = self._spacings

			nextX = x + itemW + spaceX
			if nextX - spaceX + mr > rect.right() and h > 0:
				x, y, h = rect.x() + ml, y + h + spaceY, 0
				nextX = x + itemW + spaceX

			item.setGeometry(QRect(x, y, itemW, itemH))
			x, h = nextX, max(h, itemH)

class GridFlowLayout(FlowLayout):
	def __init__(self, itemSize = 64, parent = None):
		super().__init__(parent)
		self._itemSize = itemSize

	def sizeHint(self):
		ml, mt, mr, mb = self.getContentsMargins()
		count = len(self._itemList)
		if count > 0:
			return QSize(400, 300)
		else:
			return self.minimumSize()

	def minimumSize(self):
		ml, mt, mr, mb = self.getContentsMargins()
		return QSize(self._itemSize + ml + mr, self._itemSize + mt + mb)

	def heightForWidth(self, width):
		ml, mt, mr, mb = self.getContentsMargins()
		spaceX, spaceY = self._spacings

		cols = (width - ml - mr + spaceX) // (self._itemSize + spaceX)
		rows = math.ceil(len(self._itemList) / cols)
		return rows * self._itemSize + (rows - 1) * spaceY + mt + mb

	def doLayout(self, rect):
		ml, mt, mr, mb = self.getContentsMargins()
		width = rect.width() - ml - mr
		spaceX, spaceY = self._spacings

		count = len(self._itemList)
		cols = (width + spaceX) // (self._itemSize + spaceX)
		rows = math.ceil(count / cols)

		if cols > 1 and rows > 1:
			marginFac = 0.5
			delta = (width - cols * self._itemSize - (cols - 1) * spaceX) / (cols - 1 + marginFac * 2)
			spaceX += delta
			ml += delta * marginFac

		elif cols == 1:
			ml = max(ml, (rect.width() - self._itemSize) / 2)

		rx, ry = rect.x(), rect.y()
		for i in range(count):
			row = i // cols
			col = i % cols

			x = rx + ml + col * self._itemSize + col * spaceX
			y = ry + mt + row * self._itemSize + row * spaceY

			item = self._itemList[ i ]
			item.setGeometry(QRect(x, y, self._itemSize, self._itemSize))


if __name__ == '__main__':
	import sys
	from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QSlider

	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			background-color: #333;
		}
		QPushButton {
			background-color: #555;
			border: 1px solid #333;
			border-radius: 2px;
			color: #aaa;
			padding: 4px;
		}
		QPushButton:hover, QPushButton:focus {
			background-color: #666;
			color: #fff;
		}
		QPushButton:pressed, QPushButton:checked {
			background-color: #777;
			color: #fff;
		}
	''')

	flowLayout = GridFlowLayout()
	flowLayout.setContentsMargins(10, 10, 10, 10)
	flowLayout.setContentsSpacings(10, 10)
	flowLayout.setFixedItemSize(64)
	for i in range(20): flowLayout.addWidget(QPushButton(f'Btn_{i}'))

	slider = QSlider(Qt.Horizontal)
	slider.setMinimum(32)
	slider.setMaximum(128)
	slider.valueChanged.connect(flowLayout.setFixedItemSize)
	
	win = QWidget()
	layout = QVBoxLayout()
	layout.setContentsMargins(0, 0, 0, 0)
	layout.setSpacing(0)
	layout.addLayout(flowLayout)
	layout.addWidget(slider)

	win.setLayout(layout)
	win.setWindowTitle('Flow Layout')
	win.show()
	sys.exit(app.exec())
