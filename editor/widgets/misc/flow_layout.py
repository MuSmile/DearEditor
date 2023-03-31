from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QLayout, QPushButton, QSizePolicy, QWidget

class FlowLayout(QLayout):
	def __init__(self, parent = None, margin = 0, spacingH = 0, spacingV = 0):
		super().__init__(parent)
		self.setContentsMargins(margin, margin, margin, margin)
		# self.setSpacing(spacing)
		self.spacings = (spacingH, spacingV)
		self.itemList = []

	def __del__(self):
		item = self.takeAt(0)
		while item: item = self.takeAt(0)

	def addItem(self, item):
		self.itemList.append(item)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList[index]
		else:
			return None

	def takeAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList.pop(index)
		else:
			return None

	def expandingDirections(self):
		return Qt.Orientations(Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self.doLayout(QRect(0, 0, width, 0), True)

	def setGeometry(self, rect):
		super().setGeometry(rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QSize()
		for item in self.itemList: size = size.expandedTo(item.minimumSize())
	
		m1, m2, m3, m4 = self.getContentsMargins()
		size += QSize(m1 + m3, m2 + m4)
		return size

	def doLayout(self, rect, testOnly):
		x = rect.x()
		y = rect.y()
		lineHeight = 0

		for item in self.itemList:
			wid = item.widget()
			spaceX, spaceY = self.spacings
			nextX = x + item.sizeHint().width() + spaceX
			if nextX - spaceX > rect.right() and lineHeight > 0:
				x = rect.x()
				y = y + lineHeight + spaceY
				nextX = x + item.sizeHint().width() + spaceX
				lineHeight = 0

			if not testOnly:
				item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	flowLayout = FlowLayout(spacingH = 10, spacingV = 5)
	flowLayout.addWidget(QPushButton("Short"))
	flowLayout.addWidget(QPushButton("Longer"))
	flowLayout.addWidget(QPushButton("Different text"))
	flowLayout.addWidget(QPushButton("More text"))
	flowLayout.addWidget(QPushButton("Even longer button text"))

	win = QWidget()
	win.setLayout(flowLayout)
	win.setWindowTitle("Flow Layout")
	win.show()
	sys.exit(app.exec())