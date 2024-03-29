import os, json, uuid
import xml.etree.ElementTree as ET
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import QMenu
from editor.common.logger import warn, error
from editor.common.icon_cache import getThemeIcon
from editor.common.util import getIde, isParentOfWidget
from editor.widgets.dock import CDockManager, CDockWidget, DockWidgetArea
from editor.widgets.misc.toast import Toast
import shiboken6

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
	def __init__(self, parent, **data):
		cls       = self.__class__.__name__
		name      = data['name'     ] if 'name'      in data else cls
		icon      = data['icon'     ] if 'icon'      in data else None
		title     = data['title'    ] if 'title'     in data else name
		tooltip   = data['tooltip'  ] if 'tooltip'   in data else None
		keepAlive = data['keepAlive'] if 'keepAlive' in data else False

		super().__init__(title, parent) 
		self.guid = uuid.uuid1().hex
		self.setObjectName(f'{name}::{self.guid}')

		if icon: self.setIcon(getThemeIcon(icon))
		self.setFeature(CDockWidget.DockWidgetForceCloseWithArea, True)
		self.setFeature(CDockWidget.DockWidgetDeleteOnClose, not keepAlive)
		self.setTabToolTip(tooltip)

		self.setupTitleActions()
		self.setTitleBarActions(self.actions())
		self.notification = None

	def createTitleAction(self, icon, callback, tooltip = None):
		action = QAction(self)
		action.setIcon(getThemeIcon(icon))
		action.setAutoRepeat(False)
		if callback: action.triggered.connect(callback)
		if tooltip: action.setToolTip(tooltip)
		self.addAction(action)
		return action

	def setupTitleActions(self):
		self.createTitleAction('menu_d.png', self.popupDockMenu)

	def popupDockMenu(self):
		menu = QMenu(self)
		menu.addAction("Item 1")
		menu.addAction("Item 2")
		menu.addAction("Item 3")
		menu.popup(QCursor.pos())

	def showNotification(self, msg):
		if self.notification and shiboken6.isValid(self.notification): self.notification.close()
		self.notification = Toast(msg, self)
		self.notification.show()

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

def dockView(name, icon = None, **data):
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

def createDockManager(mainWin):
	CDockManager.setConfigFlag(CDockManager.RetainTabSizeWhenCloseButtonHidden, True)
	CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetTitle, False)
	CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetIcon, False)
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
	CDockManager.setConfigFlag(CDockManager.DragPreviewShowsContentPixmap, False)

	CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideFeatureEnabled, True)
	CDockManager.setAutoHideConfigFlag(CDockManager.DockAreaHasAutoHideButton, True)
	CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideTitleForceHasCloseBtn, True)

	global _dockManager
	_dockManager = CDockManager(mainWin)
	_dockManager.setStyleSheet(None)
	_dockManager.floatingWidgetCreated.connect(lambda f: f.layout().setContentsMargins(0, 1, 0, 0))
	
	def focusedDockWidgetChanged(old, now):
		focused = getIde().focusWidget()
		if not isParentOfWidget(now, focused): now.setFocus()
		# container = now.dockContainer()
		# if container and container.isFloating(): now.window().setWindowTitle(now.tabWidget().text())

	_dockManager.focusedDockWidgetChanged.connect(focusedDockWidgetChanged)
	
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
			
			if view not in _viewRegistry:
				error(f'skip restoring view \'{view}\', which is not registered.')
				for dock in findDockViewList(view): dock.closeDockWidget()
				continue

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
