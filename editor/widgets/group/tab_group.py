from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPalette
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QStyle, QStyleOptionFrame, QSizePolicy
from editor.widgets.basic.enum_buttons import EnumButtons
from editor.widgets.complex.sliding_stacked import SlidingStackedWidget

class TabGroup(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(0)
		
		tabs = EnumButtons()
		tabs.setEnums([f'Tab {i}' for i in range(4)])
		tabs.selectEnum('Tab 0')

		stacked = SlidingStackedWidget()
		stacked.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		tabs.group.idClicked.connect(stacked.slideInIdx)
		self.container = stacked

		layout.addWidget(tabs)
		layout.addWidget(stacked)
		self.setLayout(layout)

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)

		rect = self.rect()
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.fillRect(rect, palette.color(QPalette.Base))

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)
