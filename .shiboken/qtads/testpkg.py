import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from dist import *

class DockWidget(CDockWidget):
	def __init__(self, title, parent = None):
		super().__init__(title, parent)

	def mousePressEvent(self, evt):
		super().mousePressEvent(evt)
		print('mouse pressed')

app = QApplication(sys.argv)
win = QMainWindow()
win.resize(600, 400)

toolBar = QToolBar()
toolBar.addWidget(QPushButton('label_1'))
toolBar.addWidget(QPushButton('label_2'))
toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
toolBar.setFloatable(False)
toolBar.setMovable(False)
win.addToolBar(toolBar)

CDockManager.setConfigFlag(CDockManager.OpaqueSplitterResize, True)
# CDockManager.setConfigFlag(CDockManager.OpaqueTabDragging, True)
CDockManager.setConfigFlag(CDockManager.AlwaysShowTabs, True)
CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetTitle, False)

print(CDockManager.eAutoHideFlag)
# import inspect
# print(inspect.getmembers(CDockManager.eAutoHideFlag))
print(CDockManager.eAutoHideFlag.DockAreaHasAutoHideButton)
print(CDockManager.eAutoHideFlag.__getattribute__(CDockManager.eAutoHideFlag, 'DockAreaHasAutoHideButton'))
CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideFeatureEnabled, True)
CDockManager.setAutoHideConfigFlag(CDockManager.DockAreaHasAutoHideButton, True)
CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideShowOnMouseOver, True)

dockMgr = CDockManager(win)

dock1 = CDockWidget('simple dock')
dockMgr.addDockWidget(DockWidgetArea.LeftDockWidgetArea, dock1)
# dockMgr.addAutoHideDockWidget(SideBarLocation.SideBarLeft, dock1)

dock2 = DockWidget('press me')
dockContainer = dockMgr.addDockWidgetFloating(dock2)
dockContainer.resize(300, 200)

dock3 = CDockWidget('dock 3')
dockMgr.addDockWidget(DockWidgetArea.RightDockWidgetArea, dock3)

win.show()
app.exec()