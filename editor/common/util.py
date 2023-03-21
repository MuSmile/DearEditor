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
def modelIndexDepth(index):
	"""Calculate depth of a QModelIndex.
	
	Args:
		QModelIndex index: Given index to calculate.

	Returns:
		int: depth of given QModelIndex.
	"""
	depth = 0
	parent = index.parent()
	while parent.isValid():
		depth += 1
		parent = parent.parent()
	return depth

def modelIndexRowSequence(index):
	"""Calculate row number sequence of a QModelIndex.
	
	Args:
		QModelIndex index: Given index to calculate.

	Returns:
		list[int]: number sequence of given QModelIndex.
	"""
	seq = []
	curr = index
	while curr.isValid():
		seq.insert(0, curr.row())
		curr = curr.parent()
	return seq

def isAboveOfModelIndex(test, index):
	"""Check a given QModelIndex is above of another in model.
	
	Args:
		QModelIndex test: Given QModelIndex to check.
		QModelIndex index: Given QModelIndex to check against.

	Returns:
		bool: Weather given QModelIndex is above of another or not.
	"""
	seq1 = modelIndexRowSequence(test)
	seq2 = modelIndexRowSequence(index)
	len1 = len(seq1)
	len2 = len(seq2)
	for i in range(min(len1, len2)):
		row1 = seq1[i]
		row2 = seq2[i]
		if row1 < row2: return True
		if row1 > row2: return False
	return len1 < len2

def isChildOfModelIndex(test, index):
	"""Check a given QModelIndex is child of another.
	
	Args:
		QModelIndex test: Given QModelIndex to check.
		QModelIndex index: Given QModelIndex to check against.

	Returns:
		bool: Weather given QModelIndex is child of another or not.
	"""
	p = test.parent()
	while p.isValid():
		if p == index: return True
		p = p.parent()
	return False

def isParentOfWidget(test, widget):
	"""Check a given qt widget is parent of another.
	
	Args:
		QWidget test: Given widget to check.
		QWidget widget: Given widget to check against.

	Returns:
		bool: Weather given qt widget is parent of another or not.
	"""
	if not widget: return False
	if not test: return False
	p = widget.parent()
	while p:
		if p == test: return True
		p = p.parent()
	return False

def createTestMenu(parent):
	"""Create a simple QMenu for test usage.
	
	Args:
		QWidget parent: QMenu's parent.

	Returns:
		QMenu: Required test menu.
	"""
	menu = QMenu(parent)
	menu.addAction("Item 1")
	menu.addAction("Item 2")
	menu.addAction("Item 3")
	return menu


#############################################
def toInt(text, default = 0):
	"""Convert a text to corresponding integer.
	
	Args:
		str text: Given text to convert.
		int default: Return this value when given text is not a valid integer text.

	Returns:
		int: Converted integer from given text.
	"""
	try:
		return int(text)
	except ValueError:
		return default

def toFloat(text, default = 0):
	"""Convert a text to corresponding float number.
	
	Args:
		str text: Given text to convert.
		float default: Return this value when given text is not a valid float text.

	Returns:
		float: Converted float number from given text.
	"""
	try:
		return float(text)
	except ValueError:
		return default

def formatNumber(num):
	"""Remove the decimal point and zero of integer float, for example '.0' in 1.0.
	
	Args:
		float num: Given number to format.

	Returns:
		float|int: Formatted number from given number.
	"""
	return int(num) if num % 1 == 0 else num

#############################################
def fuzzyContains(text, subtext):
	"""Check if a text fuzzy contains another.
	
	Args:
		str text: Given text to check against.
		str subtext: Given text to check.

	Returns:
		bool: Weather text fuzzy contains subtext or not.
	"""
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
	"""Record start time of some operation. Use ``report()`` to get elapsed time since ``record()``.
	"""
	global _lastRecordTime
	_lastRecordTime = time.perf_counter()

def report():
	"""Report elapsed time since last ``record()``.

	Returns:
		float: Elapsed time in millisecond.
	"""
	return (time.perf_counter() - _lastRecordTime) * 1000


#############################################
_transparentBgPixmap = None
def requestTransparentBgPixmap():
	"""Request grid-tyle transparent background pixmap.

	Returns:
		QPixmap: Required transparent background pixmap.
	"""
	global _transparentBgPixmap
	if not _transparentBgPixmap:
		_transparentBgPixmap = QPixmap(8, 8)
		_painter = QPainter(_transparentBgPixmap)
		_painter.fillRect(0, 0, 4, 4, Qt.gray)
		_painter.fillRect(4, 4, 4, 4, Qt.gray)
		_painter.fillRect(4, 0, 4, 4, Qt.white)
		_painter.fillRect(0, 4, 4, 4, Qt.white)
	return _transparentBgPixmap

_transparentBgBrush = None
def requestTransparentBgBrush():
	"""Request grid-tyle transparent background brush.

	Returns:
		QBrush: Required transparent background brush.
	"""
	global _transparentBgBrush
	if not _transparentBgBrush:
		pixmap = requestTransparentBgPixmap()
		_transparentBgBrush = QBrush(pixmap)
	return _transparentBgBrush


#############################################
def shakeWidget(target):
	"""Apply simple position shaking animation on specified target.

	Args:
		QWidget target: Given target widget to shake.
	"""
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
