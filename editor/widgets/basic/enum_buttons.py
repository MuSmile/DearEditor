from PySide6.QtWidgets import QWidget, QPushButton, QButtonGroup, QHBoxLayout

class EnumButtons(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)
		self.setLayout(layout)

	def setEnums(self, enums):
		count = len(enums)
		layout = self.layout()
		for i in range(count):
			btn = QPushButton(enums[i])
			btn.setCheckable(True)
			layout.addWidget(btn)
			self.group.addButton(btn, i)
			if i == 0: btn.setObjectName('enum_left')
			elif i == count - 1: btn.setObjectName('enum_right')
			else: btn.setObjectName('enum_middle')
		self.enums = enums

	def selectEnum(self, enum):
		idx = self.enums.index(enum)
		self.group.button(idx).setChecked(True)