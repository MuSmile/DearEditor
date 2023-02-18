import os, re, time, platform
from PySide6.QtCore import QSettings, QFile, QTextStream
from PySide6.QtWidgets import QApplication

from pathlib import Path
from editor.common.logger import log
from editor.common.file_watcher import RegexWatcher


_themeFolder = os.environ[ 'DEAR_THEME_PATH' ]
_activeTheme = None
_lastModifyTime = 0


#####################  UTILS  #####################
def _gatherStyleSheets(name):
	qssDir = f'{_themeFolder}/{name}/qss/'
	qssFiles = {}
	for currDir, dirs, files in os.walk(qssDir):
		if currDir.endswith('__qsscache__'): continue
		for f in files: qssFiles[f] = os.path.join(currDir, f)

	qssFiles = dict(sorted(qssFiles.items(), key = lambda kv: kv[1]))
	return qssFiles

def _parseSingleQss(srcPath, cachePath, sysParser, macroParser, urlParser):
	srcFile = QFile(srcPath)
	srcFile.open(QFile.ReadOnly | QFile.Text)
	srcText = QTextStream(srcFile).readAll()
	srcFile.close()

	parsed = re.sub(r'/\*.*?\*/', '', srcText, flags = re.S)
	parsed = re.sub(r'\n+', '\n', parsed, flags = re.S)
	parsed = re.sub(r'#if\s+(\S+)\s*\n(.*?)\n\s*#end', sysParser, parsed, flags = re.S)
	parsed = re.sub(r'&\[(.*)\]', macroParser, parsed)
	parsed = re.sub(r'url\((.*)\)', urlParser, parsed)

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
	if rootPath in mfilePath.parents: loadTheme(_activeTheme)

	_lastModifyTime = currTime


######################  APIS  #####################
def listThemes():
	return [ f.name for f in os.scandir(_themeFolder) if f.is_dir() ]

def activeTheme():
	return _activeTheme

def activeThemeFolder():
	return f'{_themeFolder}/{_activeTheme}'

def loadTheme(name):
	assert name in listThemes()
	global _activeTheme
	_activeTheme = name
	theme = _parseTheme(name)
	qApp = QApplication.instance()
	qApp.setStyleSheet(theme)

def setupThemeWatcher():
	global watcher
	ignores = ['.*__qsscache__.*', '.*img.*']
	watcher = RegexWatcher(ignoreRegexes = ignores, onModified = _onThemeModified)
	watcher.start(_themeFolder)


######################  TEST  #####################
if __name__ == '__main__':
	print(_gatherStyleSheets('dark'))
	# print(_parseTheme('dark'))
