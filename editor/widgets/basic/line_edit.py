from PySide6.QtWidgets import QLineEdit

class LineEdit(QLineEdit):
	def __init__(self, text = None, parent = None):
		super().__init__(text, parent)
		self.prevTextEmpty = not bool(text)
		self.textChanged.connect(self.onTextChanged)

	def onTextChanged(self):
		empty = not bool(self.text())
		if empty == self.prevTextEmpty: return
		self.prevTextEmpty = empty
		self.style().polish(self)