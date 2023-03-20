"""This module provides theme manage functions.

Typical usage example:

.. code-block:: python
   :linenos:

   from editor import theme_manager
   theme_manager.loadTheme('dark')
   theme_manager.setupThemeWatcher()
"""

import os, re, time, platform
from PySide6.QtCore import QSettings, QTimer

from pathlib import Path
from editor.common.logger import log
from editor.common.file_watcher import RegexWatcher
from editor.common.util import getIde


_themeFolder = os.environ[ 'DEAR_THEME_PATH' ]
_themeWatcher = None
_activeTheme = None
_lastModifyTime = 0


#####################  UTILS  #####################
def _gatherStyleSheets(name):
	qssDir = f'{_themeFolder}/{name}/qss/'
	qssFiles = {}
	for currDir, dirs, files in os.walk(qssDir):
		if currDir.endswith('__qsscache__'): continue
		for f in files:
			if not f.endswith('.qss'): continue
			qssFiles[f] = os.path.join(currDir, f)

	qssFiles = dict(sorted(qssFiles.items(), key = lambda kv: kv[1]))
	return qssFiles

def _parseSingleQss(srcPath, cachePath, sysParser, macroParser, urlParser):
	srcText = None
	with open(srcPath, 'r') as file:
		srcText = file.read()
		file.close()

	parsed = re.sub(r'/\*.*?\*/', '', srcText, flags = re.S)
	parsed = re.sub(r'\n+', '\n', parsed, flags = re.S)
	parsed = re.sub(r'#if\s+(\S+)\s*\n(.*?)\n\s*#end', sysParser, parsed, flags = re.S)
	parsed = re.sub(r'&\[(.*)\]', macroParser, parsed)
	parsed = re.sub(r'url\((.*)\)', urlParser, parsed)

	with open(cachePath, 'w') as file:
		file.write(parsed)
		file.close()
		# log(f'{qss} parsed successfully!'

	return parsed

def _mergeGeneratedQss(name):
	cacheDir = f'{_themeFolder}/{name}/qss/__qsscache__'

	mergedText = ''
	for f in _gatherStyleSheets(name):
		qssPath = f'{cacheDir}/{f}'
		with open(qssPath, 'r') as file:
			mergedText += file.read()
			file.close()

	return mergedText

def _gatherDirtyItems(name):
	cacheDir = f'{_themeFolder}/{name}/qss/__qsscache__'
	qssTable = _gatherStyleSheets(name)
	if not os.path.isdir(cacheDir):
		os.makedirs(cacheDir)
		return qssTable

	needReparse = {}
	settingPath = f'{_themeFolder}/{name}/macro'
	getmtime = os.path.getmtime
	mtSetting = getmtime(settingPath)

	for qssName, qssPath in qssTable.items():
		cachePath = f'{cacheDir}/{qssName}'
		if not os.path.isfile(cachePath):
			needReparse[qssName] = qssPath
		else:
			mtSrc = getmtime(qssPath)
			mtCache = getmtime(cachePath)
			if mtCache < mtSrc or mtCache < mtSetting:
				needReparse[qssName] = qssPath
	return needReparse

def _parseTheme(name):
	items = _gatherDirtyItems(name)
	if items:
		settingPath = f'{_themeFolder}/{name}/macro'
		themeSetting = QSettings(settingPath, QSettings.IniFormat)

		macroParser = lambda m: themeSetting.value(m.group(1))
		urlParser = lambda m: f'url({_themeFolder}/{name}/{m.group(1)})'
		sysParser = lambda m: m.group(2) if m.group(1) == platform.system() else ''

		for qssName, qssPath in items.items():
			cachePath = f'{_themeFolder}/{name}/qss/__qsscache__/{qssName}'
			_parseSingleQss(qssPath, cachePath, sysParser, macroParser, urlParser)

	return _mergeGeneratedQss(name)

def _onThemeModified(evt):
	global _lastModifyTime
	currTime = time.time()
	if currTime - _lastModifyTime <= 0.1: return

	log('theme modify checked, reloading theme...')
	rootPath = Path(os.path.abspath(activeThemeFolder()))
	mfilePath = Path(os.path.abspath(evt.src_path))
	if rootPath in mfilePath.parents:
		reloadTheme = lambda: loadTheme(_activeTheme, True)
		QTimer.singleShot(10, reloadTheme)

	_lastModifyTime = currTime


######################  APIS  #####################
def listThemes():
	"""List all available themes.

	Returns:
		list[str]: All available themes.
	"""
	return [ f.name for f in os.scandir(_themeFolder) if f.is_dir() ]

def activeTheme():
	"""Get current active theme.

	Returns:
		str: Active theme name.
	"""
	return _activeTheme

def activeThemeFolder():
	"""Get current active theme source folder.
	
	Returns:
		str: Active theme folder path.
	"""
	return f'{_themeFolder}/{_activeTheme}'

def loadTheme(name, reset = False):
	"""Load theme by certain name.
	
	Args:
		str name: Theme name to load.
		bool reset: Reset exsiting style state. (Mainly used by theme watcher for hot-reloading usage.)
	"""
	assert name in listThemes()
	global _activeTheme
	_activeTheme = name

	initScript = f'{_themeFolder}/{name}/init.py'
	if os.path.exists(initScript): exec(open(initScript).read())

	ide = getIde()
	if reset: ide.setStyleSheet(None)
	ide.setStyleSheet(_parseTheme(name))

def setupThemeWatcher():
	"""Setup theme watcher on all themes.
	"""
	global _themeWatcher # to keep alive
	ignores = ['.*__qsscache__.*', '.*img.*']
	_themeWatcher = RegexWatcher(ignoreRegexes = ignores, onModified = _onThemeModified)
	_themeWatcher.start(_themeFolder)

def disposeThemeWatcher():
	"""Shutdown current theme watcher
	"""
	global _themeWatcher
	if not _themeWatcher: return
	_themeWatcher.stop()
	_themeWatcher = None

######################  TEST  #####################
if __name__ == '__main__':
	print(_gatherStyleSheets('dark'))
	# print(_parseTheme('dark'))
