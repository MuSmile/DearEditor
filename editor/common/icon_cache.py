"""This module provide theme related icon/pixmap cache toolkit.
"""

from PySide6.QtGui import QIcon, QPixmap
from editor.theme_manager import activeThemeFolder


##################################################
_iconEmpty = QIcon()
def getEmptyIcon():
	"""Get empty icon, which means ``QIcon()``.

	Returns:
		QIcon: empty icon object.
	"""
	return _iconEmpty


##################################################
_themeIconCaches = {}
def getThemeIcon(path):
	"""Get icon cache of certain path.

	Args:
		str path: Icon path, related to theme folder.

	Returns:
		QIcon: Icon object of path.
	"""
	if path in _themeIconCaches: return _themeIconCaches[ path ]
	fullpath = f'{activeThemeFolder()}/img/{path}'
	icon = QIcon(fullpath)
	_themeIconCaches[ path ] = icon
	return icon

def releaseThemeIconCache():
	"""Clear all theme icon cache
	"""
	_themeIconCaches.clear()


##################################################
_themePixmapCaches = {}
def getThemePixmap(path):
	"""Get pixmap cache of certain path.

	Args:
		str path: Pixmap path, related to theme folder.

	Returns:
		QPixmap: Pixmap object of path.
	"""
	if path in _themePixmapCaches: return _themePixmapCaches[ path ]
	fullpath = f'{activeThemeFolder()}/img/{path}'
	pixmap = QPixmap(fullpath)
	_themePixmapCaches[ path ] = pixmap
	return pixmap

def releaseThemePixmapCache():
	"""Clear all theme pixmap cache
	"""
	_themePixmapCaches.clear()