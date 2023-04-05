from PySide6.QtWidgets import QWidget, QPushButton, QButtonGroup, QHBoxLayout

class EnumButtons(QWidget):
	def __init__(self, enums):
		super().__init__()
		layout = QHBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)

		count = len(enums)
		for i in range(count):
			btn = QPushButton(enums[i])
			btn.setCheckable(True)
			layout.addWidget(btn)
			self.group.addButton(btn)
			if i == 0: btn.setObjectName('enum_left')
			elif i == count - 1: btn.setObjectName('enum_right')
			else: btn.setObjectName('enum_middle')

		self.setLayout(layout)
