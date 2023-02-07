import os, re, time
from PySide6.QtCore import QSettings, QFile, QTextStream
from PySide6.QtWidgets import QApplication

from pathlib import Path
from editor.common.logger import log
from editor.common.file_watcher import RegexWatcher

_themeFolder = 'themes'

def _gatherStyleSheets(name):
	qssDir = f'{_themeFolder}/{name}/qss/'
	qssFiles = {}
	for currDir, dirs, files in os.walk(qssDir):
		if currDir.endswith('__qsscache__'): continue
		for f in files: qssFiles[f] = os.path.join(currDir, f)
	return qssFiles

def _parseSingleQss(srcPath, cachePath, macroParser, urlParser):
	srcFile = QFile(srcPath)
	srcFile.open(QFile.ReadOnly | QFile.Text)
	srcText = QTextStream(srcFile).readAll()
	srcFile.close()

	parsed = re.sub(r'&\[(.*)\]', macroParser, srcText)
	parsed = re.sub(r'url\((.*)\)', urlParser, parsed)
	parsed = re.sub(r'/\*.*?\*/', '', parsed, flags = re.S)
	parsed = re.sub(r'\n+', '\n', parsed, flags = re.S)

	cacheFile = QFile(cachePath)
	cacheFile.open(QFile.WriteOnly | QFile.Text)
	stream = QTextStream(cacheFile)
	stream << parsed
	cacheFile.close()
	# log(f'{qss} parsed successfully!'

	return parsed

def _mergeGeneratedQss(name):
	cacheDir = f'{_themeFolder}/{name}/qss/__qsscache__'

	mergedText = ''
	for f in _gatherStyleSheets(name):
		qssPath = f'{cacheDir}/{f}'
		qssFile = QFile(qssPath)
		qssFile.open(QFile.ReadOnly | QFile.Text)
		qssText = QTextStream(qssFile).readAll()
		qssFile.close()
		mergedText += qssText

	return mergedText

def _gatherItemsNeedToReparse(name):
	cacheDir = f'{_themeFolder}/{name}/qss/__qsscache__'
	qssTable = _gatherStyleSheets(name)
	if not os.path.isdir(cacheDir):
		os.makedirs(cacheDir)
		return qssTable

	toReparse = {}
	settingPath = f'{_themeFolder}/{name}/macro'
	getmtime = os.path.getmtime
	mtSetting = getmtime(settingPath)

	for qssName, qssPath in qssTable.items():
		cachePath = f'{cacheDir}/{qssName}'
		if not os.path.isfile(cachePath):
			toReparse[qssName] = qssPath
		else:
			mtSrc = getmtime(qssPath)
			mtCache = getmtime(cachePath)
			if mtCache < mtSrc or mtCache < mtSetting:
				toReparse[qssName] = qssPath
	return toReparse

def _parseTheme(name):
	items = _gatherItemsNeedToReparse(name)
	if items:
		settingPath = f'{_themeFolder}/{name}/macro'
		themeSetting = QSettings(settingPath, QSettings.IniFormat)

		macroParser = lambda m: themeSetting.value(m.group(1))
		urlParser = lambda m: f'url({_themeFolder}/{name}/{m.group(1)})'

		for qssName, qssPath in items.items():
			cachePath = f'{_themeFolder}/{name}/qss/__qsscache__/{qssName}'
			_parseSingleQss(qssPath, cachePath, macroParser, urlParser)

	return _mergeGeneratedQss(name)


def listThemes():
	return [ f.name for f in os.scandir(_themeFolder) if f.is_dir() ]

_activeTheme = None
def loadTheme(name):
	assert name in listThemes()
	global _activeTheme
	_activeTheme = name
	theme = _parseTheme(name)
	qApp = QApplication.instance()
	qApp.setStyleSheet(theme)

def activeTheme():
	return _activeTheme

def activeThemeFolder():
	return f'{_themeFolder}/{_activeTheme}'

_lastModifyTime = 0
def _onThemeModified(evt):
	global _lastModifyTime
	currTime = time.time()
	if currTime - _lastModifyTime <= 0.1: return

	log('theme modify checked, reloading theme...')
	rootPath = Path(activeThemeFolder())
	mfilePath = Path(evt.src_path)
	if rootPath in mfilePath.parents: loadTheme(_activeTheme)

	_lastModifyTime = currTime

def setupThemeWatcher():
	global watcher
	ignores = ['.*__qsscache__.*', '.*img.*']
	watcher = RegexWatcher(ignoreRegexes = ignores, onModified = _onThemeModified)
	watcher.start(_themeFolder)

if __name__ == '__main__':
	print(_gatherStyleSheets('dark'))
	# print(_parseTheme('dark'))
