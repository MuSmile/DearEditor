import time
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint
from PySide6.QtGui import QPainter, QPixmap, QBrush


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
