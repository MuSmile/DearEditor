from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from editor.widgets.basic.line_edit import IntLineEdit, FloatLineEdit

class Vector2Edit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Y'))
		layout.addWidget(FloatLineEdit())
		self.setLayout(layout)

class Vector2IntEdit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addSpacing(5)
		layout.addWidget(FloatLineEdit())
		layout.addWidget(QLabel('Y'))
		layout.addWidget(FloatLineEdit())
		self.setLayout(layout)

class Vector3Edit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Y'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Z'))
		layout.addWidget(FloatLineEdit())
		self.setLayout(layout)

class Vector3IntEdit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addWidget(IntLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Y'))
		layout.addWidget(IntLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Z'))
		layout.addWidget(IntLineEdit())
		self.setLayout(layout)

class Vector4Edit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Y'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Z'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('W'))
		layout.addWidget(FloatLineEdit())
		self.setLayout(layout)

class Vector4IntEdit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QHBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(QLabel('X'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Y'))
		layout.addWidget(FloatLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('Z'))
		layout.addWidget(IntLineEdit())
		layout.addSpacing(5)
		layout.addWidget(QLabel('W'))
		layout.addWidget(IntLineEdit())
		self.setLayout(layout)

class RectEdit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QVBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)

		layout1 = QHBoxLayout()
		layout1.setSpacing(5)
		layout1.setContentsMargins(0, 0, 0, 0)
		layout1.addWidget(QLabel('X'))
		layout1.addWidget(FloatLineEdit())
		layout1.addSpacing(5)
		layout1.addWidget(QLabel('Y'))
		layout1.addWidget(FloatLineEdit())

		layout2 = QHBoxLayout()
		layout2.setSpacing(5)
		layout2.setContentsMargins(0, 0, 0, 0)
		layout2.addWidget(QLabel('W'))
		layout2.addWidget(FloatLineEdit())
		layout2.addSpacing(5)
		layout2.addWidget(QLabel('H'))
		layout2.addWidget(FloatLineEdit())

		layout.addLayout(layout1)
		layout.addLayout(layout2)
		self.setLayout(layout)

class RectIntEdit(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QVBoxLayout()
		layout.setSpacing(5)
		layout.setContentsMargins(0, 0, 0, 0)

		layout1 = QHBoxLayout()
		layout1.setSpacing(5)
		layout1.setContentsMargins(0, 0, 0, 0)
		layout1.addWidget(QLabel('X'))
		layout1.addWidget(IntLineEdit())
		layout1.addSpacing(5)
		layout1.addWidget(QLabel('Y'))
		layout1.addWidget(IntLineEdit())

		layout2 = QHBoxLayout()
		layout2.setSpacing(5)
		layout2.setContentsMargins(0, 0, 0, 0)
		layout2.addWidget(QLabel('W'))
		layout2.addWidget(IntLineEdit())
		layout2.addSpacing(5)
		layout2.addWidget(QLabel('H'))
		layout2.addWidget(IntLineEdit())

		layout.addLayout(layout1)
		layout.addLayout(layout2)
		self.setLayout(layout)
