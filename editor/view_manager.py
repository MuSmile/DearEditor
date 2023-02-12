import os, json, platform
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QEvent, QSettings, QTimer, QSize
from PySide6.QtGui import QAction
from editor.common.pyqtads import *
from editor.common.logger import warn
from editor.common.icon_cache import getThemeIcon
from editor.widgets.toast import notifyToast

_dockManager = None
_viewRegistry = {}

class DockView(CDockWidget):
	viewName  = None
	viewIcon  = None
	keepAlive = False
	minSize   = QSize(150, 100)

	def __init__(self, parent = None, title = None, icon = None):
		title = title or self.viewName
		icon  = icon  or self.viewIcon
		deledeOnClose = not self.keepAlive
		super().__init__(title, parent)
		if icon: self.setIcon(getThemeIcon(icon))
		self.setFeature(CDockWidget.DockWidgetForceCloseWithArea, True)
		self.setFeature(CDockWidget.DockWidgetDeleteOnClose, deledeOnClose)
		self.setTabToolTip(None)
		self.setupTitleActions()

	def createTitleAction(self, icon, func = None, shortcut = False, checkable = False):
		action = QAction()
		action.setAutoRepeat(False)
		if func: action.triggered.connect(func)
		if icon: action.setIcon(getThemeIcon(icon))
		if shortcut:
			action.setShortcut(shortcut)
			action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
		if checkable:
			action.setCheckable(True)
			action.setChecked(True)
		self.titleActions.append(action)

	def setupTitleActions(self):
		self.titleActions = []
		self.createTitleAction('menu_d.png')
		self.setTitleBarActions( self.titleActions )

	def showNotification(self, msg, duration = 1.5):
		notifyToast(self, msg, duration * 1000)

	def minimumSizeHint(self):
		return self.minSize

	def addIntoEditor(self, area = 'center', anchor = None):
		anchor = anchor or focusedDockView()
		if anchor:
			_dockManager.addDockWidget(_dockAreaTable[area], self, anchor.dockAreaWidget())
		else:
			_dockManager.addDockWidget(_dockAreaTable[area], self)

	def addIntoEditorAsFloating(self):
		_dockManager.addDockWidgetFloating(self)


#############################################################

# function style
def registerDockView(cls, name = None, icon = None, keepAlive = False):
	if not name: name = cls.__name__
	if name in _viewRegistry: warn(f'editor view \'{name}\' has registered!')
	cls.viewName  = name
	cls.viewIcon  = icon
	cls.keepAlive = keepAlive
	_viewRegistry[name] = cls

# decorator style
def registerView(name = None, icon = None, keepAlive = False):
	def wrapper(cls):
		registerDockView(cls, name, icon, keepAlive)
		return cls
	return wrapper


#############################################################
_dockAreaTable = {
	'left'   : DockWidgetArea.LeftDockWidgetArea,
	'right'  : DockWidgetArea.RightDockWidgetArea,
	'top'    : DockWidgetArea.TopDockWidgetArea,
	'bottom' : DockWidgetArea.BottomDockWidgetArea,
	'center' : DockWidgetArea.CenterDockWidgetArea,
}

def findDockView(name):
	return _dockManager.findDockWidget(name)

def createDockView(name):
	return _viewRegistry[name](_dockManager)

def affirmDockView(name):
	dock = findDockView(name)
	if not dock: dock = createDockView(name)
	return dock

def focusedDockView():
	return _dockManager.focusedDockWidget()

def closeFocusedDockView():
	focused = _dockManager.focusedDockWidget()
	if focused: focused.closeDockWidget()

def setDockViewFocused(name, focused):
	dock = findDockView(name)
	_dockManager.setDockWidgetFocused(focused)
	dock.setAsCurrentTab()

def setDockSplitterSizes(dockArea, sizes):
	_dockManager.setSplitterSizes(dockArea, sizes)

def createDockManager(parent):
	CDockManager.setConfigFlag(CDockManager.RetainTabSizeWhenCloseButtonHidden, True)
	CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetIcon, False)
	CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetTitle, False)
	CDockManager.setConfigFlag(CDockManager.OpaqueSplitterResize, True)
	CDockManager.setConfigFlag(CDockManager.TabCloseButtonIsToolButton, False)
	CDockManager.setConfigFlag(CDockManager.DockAreaHasUndockButton, False)
	CDockManager.setConfigFlag(CDockManager.DockAreaHasCloseButton, False)
	CDockManager.setConfigFlag(CDockManager.DockAreaHasTabsMenuButton, False)
	CDockManager.setConfigFlag(CDockManager.ActiveTabHasCloseButton, False)
	# CDockManager.setConfigFlag(CDockManager.XmlAutoFormattingEnabled, True)
	CDockManager.setConfigFlag(CDockManager.XmlCompressionEnabled, False)
	CDockManager.setConfigFlag(CDockManager.AlwaysShowTabs, True)
	CDockManager.setConfigFlag(CDockManager.FocusHighlighting, True)
	CDockManager.setConfigFlag(CDockManager.MiddleMouseButtonClosesTab, True)
	if platform.system() == 'Darwin': CDockManager.setConfigFlag(CDockManager.AllMenusHaveCustomStyle, True)

	CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideFeatureEnabled, True)
	CDockManager.setAutoHideConfigFlag(CDockManager.DockAreaHasAutoHideButton, True)
	CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideTitleForceHasCloseBtn, True)

	global _dockManager
	_dockManager = CDockManager(parent)
	_dockManager.setStyleSheet(None)
	# _dockManager.floatingWidgetCreated.connect(lambda f: f.layout().setContentsMargins(0, 1, 0, 0))
	_dockManager.focusedDockWidgetChanged.connect(lambda old, now: now.setFocus())
	return _dockManager

def dockManager():
	return _dockManager


#############################################################
def listLayouts():
	layoutDir = 'data/layouts/'
	if not os.path.isdir(layoutDir): return
	# collect filenames which cut '.ini'
	return [ f.name[:-4] for f in os.scandir(layoutDir) if f.is_file() ]

def _collectDocksSummary(xmldata):
	summary = []
	adsTree = ET.fromstring(bytes(xmldata).decode())
	for dock in adsTree.findall('.//Widget'):
		if dock.attrib['Closed'] == '1': continue
		title = dock.attrib['Name']
		view = _dockManager.findDockWidget(title)
		summary.append({
			'Title'   : title,
			'ViewName': view.viewName
		})
	return summary

def saveLayout(name):
	# _dockManager.addPerspective(name)
	file = f'data/layouts/{name}.ini'
	setting = QSettings(file, QSettings.IniFormat)
	# print(_dockManager.saveState())
	state = _dockManager.saveState()
	summary = _collectDocksSummary(state)
	setting.setValue('Summary', json.dumps(summary))
	setting.setValue('ViewState', _dockManager.saveState())

	win = _dockManager.window()
	data = {'state' : int(win.windowState())}
	rect = win.geometry()
	data['w'] = rect.width()
	data['h'] = rect.height()
	# setting.setValue('visibility', json.dumps(mainWin.visibility()))
	setting.setValue('WindowData', json.dumps(data))

	focused = _dockManager.focusedDockWidget()
	if focused: setting.setValue('ViewFocused', focused.viewName)

def loadLayout(name):
	# _dockManager.openPerspective(name)
	# _dockManager.window().hide()
	file = f'data/layouts/{name}.ini'
	setting = QSettings(file, QSettings.IniFormat)
	summary = json.loads(setting.value('Summary'))

	toKeep = []
	toCreate = []
	for item in summary:
		title    = item['Title']
		viewName = item['ViewName']
		dock = getEditorView(title)
		if dock and dock.viewName == viewName:
			toKeep.append(dock)
		else:
			toCreate.append(item)

	for dock in _dockManager.dockWidgetsMap().values():
		if dock not in toKeep: dock.closeDockWidget()

	for item in toCreate:
		title    = item['Title']
		viewName = item['ViewName']
		tabTo = _dockManager.dockWidgetsMap().keys()[0]
		showEditorViewTabTo(viewName, tabTo)

	state = setting.value('ViewState')
	_dockManager.restoreState(bytearray(state))

	data = json.loads(setting.value('WindowData'))
	win = _dockManager.window()
	win.setWindowState(Qt.WindowState(data['state']))
	win.resize(data['w'], data['h'])

	focused = setting.value('ViewFocused')
	if focused: setDockFocused(focused)
	# QTimer.singleShot(10, win.show)


if __name__ == '__main__':
	print(listLayouts())
