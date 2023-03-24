from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextOption, QTextBlockFormat, QTextCursor, QFontMetrics
from PySide6.QtWidgets import QTextEdit
from editor.common.math import clamp

class TextArea(QTextEdit):
	def __init__(self, minLines = 4, maxLines = 9, parent = None):
		super().__init__(parent)
		self.setWordWrapMode(QTextOption.WrapAnywhere)
		textCursor = self.textCursor()
		blockFormat = textCursor.blockFormat()
		blockFormat.setLineHeight(-1, QTextBlockFormat.LineDistanceHeight)
		textCursor.setBlockFormat(blockFormat)
		self.textChanged.connect(self.onTextChanged)

		self.minLines = minLines
		self.maxLines = maxLines
		self.currLines = clamp(self.calcDocumentLines(), self.minLines, self.maxLines)
		self.setHeightByLineCount(minLines)

		self.exceedMaxLines = False
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

	def onTextChanged(self):
		docLines = self.calcDocumentLines()

		exceedMaxLines = docLines > self.maxLines
		if self.exceedMaxLines != exceedMaxLines:
			self.exceedMaxLines = exceedMaxLines
			if exceedMaxLines:
				self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			else:
				self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		dstLines = clamp(docLines, self.minLines, self.maxLines)
		if self.currLines != dstLines:
			self.currLines = dstLines
			self.setHeightByLineCount(dstLines)

	def calcDocumentLines(self):
		return self.document().size().height() // self.fontMetrics().lineSpacing()

	def setHeightByLineCount(self, rows):
		margins = self.contentsMargins()
		docMargins = self.document().documentMargin() * 2
		totalMargins = docMargins + margins.top() + margins.bottom()
		contentHeight = self.fontMetrics().lineSpacing() * rows
		self.setFixedHeight(contentHeight + totalMargins + self.frameWidth() * 2)

	def clearFocusAndSelection(self):
		cursor = self.textCursor()
		cursor.clearSelection()
		self.setTextCursor(cursor)
		self.clearFocus()

	def keyPressEvent(self, evt):
		key = evt.key()
		if key == Qt.Key_Escape: return self.clearFocusAndSelection()
		if key == Qt.Key_Return and evt.modifiers() == Qt.ControlModifier: return self.clearFocusAndSelection()
		super().keyPressEvent(evt)

	def wheelEvent(self, evt):
		super().wheelEvent(evt)
