from PySide6.QtWidgets import QFrame

def HLineWidget(color = '#222', height = 1, parent = None):
	line = QFrame(parent)
	line.setFixedHeight(height)
	line.setStyleSheet(f'background:{color};')
	line.setFrameShape(QFrame.HLine)
	return line

def VLineWidget(color = '#222', width = 1, parent = None):
	line = QFrame(parent)
	line.setFixedWidth(width)
	line.setStyleSheet(f'background:{color};')
	line.setFrameShape(QFrame.VLine)
	return line