import os, json, platform, uuid
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QAction
from editor.common.pyqtads import CDockManager, CDockWidget, DockWidgetArea
from editor.common.logger import warn, error
from editor.common.icon_cache import getThemeIcon
from editor.widgets.misc.toast import notifyToast


#######################  INTERNALS  #######################
_dockManager = None
_viewRegistry = {}
_dockAreaTable = {
	'left'   : DockWidgetArea.LeftDockWidgetArea,
	'right'  : DockWidgetArea.RightDockWidgetArea,
	'top'    : DockWidgetArea.TopDockWidgetArea,
	'bottom' : DockWidgetArea.BottomDockWidgetArea,
	'center' : DockWidgetArea.CenterDockWidgetArea,
}


#######################  INTERFACE  #######################
class DockView(CDockWidget):
	def __init__(self, parent = None, **data):
		cls       = self.__class__.__name__
		name      = data['name'     ] if 'name'      in data else cls
		icon      = data['icon'     ] if 'icon'      in data else None
		title     = data['title'    ] if 'title'     in data else name
		toolTip   = data['toolTip'  ] if 'toolTip'   in data else None
		keepAlive = data['keepAlive'] if 'keepAlive' in data else False

		super().__init__(title, parent)
		self.guid = uuid.uuid1().hex
		self.setObjectName(f'{name}::{self.guid}')

		if icon: self.setIcon(getThemeIcon(icon))
		self.setFeature(CDockWidget.DockWidgetForceCloseWithArea, True)
		self.setFeature(CDockWidget.DockWidgetDeleteOnClose, not keepAlive)
		self.setTabToolTip(toolTip)

		self.setupTitleActions()

	def createTitleAction(self, icon, func = None, shortcut = False, checkable = False):
		action = QAction()
		action.setAutoRepeat(False)
		action.setToolTip('foo')
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

	def addIntoEditor(self, area = 'center', anchor = None):
		anchor = anchor or focusedDockView()
		if anchor:
			_dockManager.addDockWidget(_dockAreaTable[area], self, anchor.dockAreaWidget())
		else:
			_dockManager.addDockWidget(_dockAreaTable[area], self)
	def addIntoEditorAsFloating(self):
		_dockManager.addDockWidgetFloating(self)

	def minimumSizeHint(self):
		return QSize(150, 100)

	def onLoadLayout(self):
		# print('dump data: ', self.serializedData())
		pass


#######################  REGISTERS  #######################
def registerDockView(cls, name, icon = None, **data):
	if name in _viewRegistry: warn(f'editor view \'{name}\' has registered!')
	
	data['icon' ] = icon
	data['name' ] = name
	data['class'] = cls
	_viewRegistry[name] = data

def registerView(name, icon = None, **data):
	def wrapper(cls):
		registerDockView(cls, name, icon, **data)
		return cls
	return wrapper


registerDockView(DockView, 'Dummy')


#########################  API  ##########################
def findDockView(name):
	dockMap = _dockManager.dockWidgetsMap()
	for k in dockMap:
		if k.startswith(name + '::'):
			return dockMap[k]
def findDockViewList(name):
	dockMap = _dockManager.dockWidgetsMap()
	list = []
	for k in dockMap:
		if k.startswith(name + '::'):
			list.append(dockMap[k])
	return list

def createDockView(name):
	data = _viewRegistry[name]
	cls  = data['class']
	return cls(_dockManager, **data)
def affirmDockView(name):
	dock = findDockView(name)
	if not dock: dock = createDockView(name)
	return dock

def focusedDockView():
	return _dockManager.focusedDockWidget()
def setDockViewFocused(name, focused):
	dock = findDockView(name)
	_dockManager.setDockWidgetFocused(focused)
	dock.setAsCurrentTab()
def closeFocusedDockView():
	focused = _dockManager.focusedDockWidget()
	if focused: focused.closeDockWidget()

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
	CDockManager.setConfigFlag(CDockManager.XmlAutoFormattingEnabled, True)
	CDockManager.setConfigFlag(CDockManager.XmlCompressionEnabled, False)
	CDockManager.setConfigFlag(CDockManager.AlwaysShowTabs, True)
	CDockManager.setConfigFlag(CDockManager.FocusHighlighting, True)
	CDockManager.setConfigFlag(CDockManager.MiddleMouseButtonClosesTab, True)
	
	if platform.system() == 'Darwin':
		CDockManager.setConfigFlag(CDockManager.AllMenusHaveCustomStyle, True)

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


#########################  LAYOUT  #########################
def listLayouts():
	folder = 'data/layouts/'
	if not os.path.exists(folder): return
	return [ f.name for f in os.scandir(folder) if f.is_dir() ]

def saveLayout(name):
	folder = f'data/layouts/{name}/'
	if not os.path.exists(folder): os.makedirs(folder)

	statesFile = folder + 'states.xml'
	windowFile = folder + 'window.json'

	with open(statesFile, 'wb') as file:
		file.write(bytes(_dockManager.saveState(1)))
		file.close()

	# enum Qt.WindowState:
	# ------------------------------------
	#    Qt.WindowNoState     0x00000000
	#    Qt.WindowMinimized   0x00000001
	#    Qt.WindowMaximized   0x00000002
	#    Qt.WindowFullScreen  0x00000004
	#    Qt.WindowActive      0x00000008

	with open(windowFile, 'w') as file:
		win = _dockManager.window()
		rect = win.geometry()
		file.write(json.dumps({
			'state' : int(win.windowState()),
			'width' : rect.width(),
			'height': rect.height(),
		}, indent = 4))
		file.close()

def loadLayout(name):
	folder = f'data/layouts/{name}/'
	if not os.path.exists(folder): return error(f'load layout fail! layout \'{name}\' not found.')

	statesFile = folder + 'states.xml'
	windowFile = folder + 'window.json'

	with open(statesFile, 'rb') as file:
		states = bytearray(file.read())
		file.close()

		layoutTable = {}
		adsTree = ET.fromstring(bytes(states).decode())
		for dock in adsTree.findall('.//Widget'):
			if dock.attrib['Closed'] == '1': continue
			names = dock.attrib['Name'].split('::')
			view, guid = names[0], names[1]
			data = {
				'guid': guid,
				'name': dock.attrib['Name'],
				'data': dock.attrib['Data'] if 'Data' in dock.attrib else None
			}
			if view in layoutTable:
				layoutTable[ view ].append(data)
			else:
				layoutTable[ view ] = [ data ]

		for view in layoutTable:
			lviews = layoutTable[view]
			eviews = findDockViewList(view)
			lviewsLen, eviewsLen = len(lviews), len(eviews)
				
			def insideLayout(name):
				for table in lviews:
					if table['name'] == name:
						return True
				return False

			if lviewsLen > eviewsLen:
				for i in range(eviewsLen, lviewsLen):
					new = createDockView(view)
					new.addIntoEditor()
					eviews.append(new)
			
			elif lviewsLen < eviewsLen:
				closeIndexList = []
				closeCount = eviewsLen - lviewsLen
				for i in range(eviewsLen):
					if not insideLayout(eviews[i].objectName()): closeIndexList.insert(0, i)
					if len(closeIndexList) == closeCount: break
				for i in closeIndexList:
					eviews[i].closeDockWidget()
					del eviews[i]

			stayTable, reuseList = {}, []
			for dock in eviews:
				name = dock.objectName()
				if insideLayout(name):
					stayTable[name] = dock
				else:
					reuseList.append(dock)

			for i in range(0, lviewsLen):
				table = lviews[i]
				dockWidget = None
				name = table['name']
				if name in stayTable:
					dockWidget = stayTable[name]
				else:
					dockWidget = reuseList.pop()
					oldName = dockWidget.objectName()
					dockWidget.setObjectName(name)
					_dockManager.updateDockWidgetsMapKey(oldName, name)
				
		_dockManager.restoreState(states, 1)
		for container in _dockManager.dockContainers():
			for i in range(container.dockAreaCount()):
				# hided for fixing flashing issue in restore phase,
				# so, we need re-show it now... very stupid...
				area = container.dockArea(i)
				area.show()
		for d in _dockManager.dockWidgetsMap().values(): d.onLoadLayout()

	win = _dockManager.window()
	with open(windowFile, 'r') as file:
		windata = json.loads(file.read())
		file.close()

		win.setWindowState(Qt.WindowState(windata['state']))
		win.resize(windata['width'], windata['height'])

	win.activateWindow()
	win.raise_()


######################  TEST  ######################
from editor.widgets.menubar import menuItem

@menuItem('Tools/test save layout')
def testSaveLayout(): saveLayout('test')

@menuItem('Tools/test load layout')
def testLoadLayout(): loadLayout('test')

# print(listLayouts())
