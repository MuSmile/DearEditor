from PySide6.QtGui import QIcon, QPixmap
from editor.theme_manager import activeThemeFolder


##################################################
_iconEmpty = QIcon()
def getEmptyIcon(): return _iconEmpty


##################################################
_themeIconCaches = {}
def getThemeIcon(path):
	if path in _themeIconCaches: return _themeIconCaches[ path ]
	fullpath = f'{activeThemeFolder()}/img/{path}'
	icon = QIcon(fullpath)
	_themeIconCaches[ path ] = icon
	return icon

def releaseThemeIconCache():
	_themeIconCaches.clear()


##################################################
_themePixmapCaches = {}
def getThemePixmap(path):
	if path in _themePixmapCaches: return _themePixmapCaches[ path ]
	fullpath = f'{activeThemeFolder()}/img/{path}'
	pixmap = QPixmap(fullpath)
	_themePixmapCaches[ path ] = pixmap
	return pixmap

def releaseThemePixmapCache():
	_themePixmapCaches.clear()