from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QFrame, QListWidgetItem
from PySide6.QtGui import QColor

def HLineWidget(parent = None, color = '#333', height = 2):
	line = QFrame(parent)
	line.setFixedHeight(height)
	line.setStyleSheet(f'background:{color};')
	line.setFrameShape(QFrame.HLine)
	return line

def VLineWidget(parent = None, color = '#333', width = 2):
	line = QFrame(parent)
	line.setFixedWidth(width)
	line.setStyleSheet(f'background:{color};')
	line.setFrameShape(QFrame.VLine)
	return line

def QListWidgetLineItem(height = 1, background = QColor('#888')):
    line = QListWidgetItem(None, -1)
    line.setFlags(Qt.NoItemFlags)
    line.setBackground(background)
    line.setSizeHint(QSize(0, height))
    return line