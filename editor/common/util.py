"""This module provides uncategorized misc toolkit.
"""

import sys, os, time
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QPainter, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu


#############################################
_ide = None
def getIde():
	"""Get DearEditor ide instance.
	
	Returns:
		QApplication: The instance of Ide/QApplication.
	"""
	global _ide
	if not _ide: _ide = QApplication.instance()
	return _ide

def getMainWindow():
	"""Get DearEditor ide main window instance.
	
	Returns:
		QMainWindow: The instance of ide's main window.
	"""
	app = QApplication.instance()
	for widget in app.topLevelWidgets():
		if isinstance(widget, QMainWindow):
			return widget

def restartApp():
	"""Restart DearEditor ide.
	"""
	quitApp()
	py = sys.executable
	os.execl(py, py, *sys.argv)

def quitApp():
	"""Exit DearEditor ide.
	"""
	getMainWindow().close()


#############################################
def isParentOfWidget(test, wgt):
	"""Check a given qt widget is parent of another.
	
	Args:
		QWidget test: Given widget to check.
		QWidget wgt: Given widget to check against.

	Returns:
		bool: Weather given qt widget is parent of another or not.
	"""
	if not wgt: return False
	if not test: return False
	p = wgt.parent()
	while p:
		if p == test: return True
		p = p.parent()
	return False

def createTestMenu(parent):
	menu = QMenu(parent)
	menu.addAction("Item 1")
	menu.addAction("Item 2")
	menu.addAction("Item 3")
	return menu


#############################################
def toInt(text, default = 0):
	try:
		return int(text)
	except ValueError:
		return default
def toFloat(text, default = 0.0):
	try:
		return float(text)
	except ValueError:
		return default


#############################################
def fuzzyContains(str, substr):
	len1, len2 = len(str), len(substr)
	if len1 < len2: return False
	if len1 == len2 and str == substr: return True
	pos = 0
	for c in substr:
		idx = str.find(c, pos)
		if idx < 0: return False
		pos = idx + 1
	return True


#############################################
_lastRecordTime = None
def record():
	global _lastRecordTime
	_lastRecordTime = time.perf_counter()

def report():
	return (time.perf_counter() - _lastRecordTime) * 1000


#############################################
_transparentBgPixmap = None
_transparentBgBrush = None
def requestTransparentBgPixmap():
	global _transparentBgPixmap
	if not _transparentBgPixmap:
		_transparentBgPixmap = QPixmap(8, 8)
		_painter = QPainter(_transparentBgPixmap)
		_painter.fillRect(0, 0, 4, 4, Qt.gray)
		_painter.fillRect(4, 4, 4, 4, Qt.gray)
		_painter.fillRect(4, 0, 4, 4, Qt.white)
		_painter.fillRect(0, 4, 4, 4, Qt.white)
	return _transparentBgPixmap
def requestTransparentBgBrush():
	global _transparentBgBrush
	if not _transparentBgBrush:
		pixmap = requestTransparentBgPixmap()
		_transparentBgBrush = QBrush(pixmap)
	return _transparentBgBrush


#############################################
def shakeWidget(target):
	if hasattr(target, '_shakeing'): return
	animation = QPropertyAnimation(target, b'pos', target)
	animation.finished.connect(lambda: delattr(target, '_shakeing'))
	target._shakeing = True
	pos = target.pos()
	x, y = pos.x(), pos.y()
	animation.setDuration(100)
	animation.setLoopCount(2)
	animation.setKeyValueAt(0, QPoint(x, y))
	animation.setKeyValueAt(0.09, QPoint(x + 1, y - 1))
	animation.setKeyValueAt(0.18, QPoint(x + 2, y - 2))
	animation.setKeyValueAt(0.27, QPoint(x + 1, y - 3))
	animation.setKeyValueAt(0.36, QPoint(x + 0, y - 4))
	animation.setKeyValueAt(0.45, QPoint(x - 1, y - 3))
	animation.setKeyValueAt(0.54, QPoint(x - 2, y - 4))
	animation.setKeyValueAt(0.63, QPoint(x - 3, y - 3))
	animation.setKeyValueAt(0.72, QPoint(x - 4, y - 2))
	animation.setKeyValueAt(0.81, QPoint(x - 3, y - 1))
	animation.setKeyValueAt(0.90, QPoint(x - 2, y - 0))
	animation.setKeyValueAt(0.99, QPoint(x - 1, y + 1))
	animation.setEndValue(QPoint(x, y))
	animation.start(animation.DeleteWhenStopped)
