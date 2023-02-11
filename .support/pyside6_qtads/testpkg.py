import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from dist import *

class _DockWidget(CDockWidget):
	def __init__(self, title, parent = None):
		super().__init__(title, parent)

	def mousePressEvent(self, evt):
		super().mousePressEvent(evt)
		print('mouse pressed')

class _QMainWindow(QMainWindow):
	def closeEvent(self, evt):
		for fw in self.dockMgr.floatingWidgets(): fw.close()
		super().closeEvent(evt)

app = QApplication(sys.argv)
win = _QMainWindow()
win.resize(600, 400)

toolBar = QToolBar()
label1 = QPushButton('label_1')
label2 = QPushButton('label_2')
toolBar.addWidget(label1)
toolBar.addWidget(label2)
toolBar.addWidget(QLabel('test'))
toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
toolBar.setFloatable(False)
toolBar.setMovable(False)
win.addToolBar(toolBar)

CDockManager.setConfigFlag(CDockManager.OpaqueSplitterResize, True)
# CDockManager.setConfigFlag(CDockManager.OpaqueTabDragging, True)
CDockManager.setConfigFlag(CDockManager.AlwaysShowTabs, True)
CDockManager.setConfigFlag(CDockManager.FloatingContainerHasWidgetTitle, False)
CDockManager.setConfigFlag(CDockManager.DockAreaHasUndockButton, False)
CDockManager.setConfigFlag(CDockManager.DockAreaHasCloseButton, False)
CDockManager.setConfigFlag(CDockManager.DockAreaHasTabsMenuButton, False)

# print(CDockManager.eAutoHideFlag.DockAreaHasAutoHideButton)
# print(CDockManager.eAutoHideFlag.__getattribute__(CDockManager.eAutoHideFlag, 'DockAreaHasAutoHideButton'))
CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideFeatureEnabled, True)
CDockManager.setAutoHideConfigFlag(CDockManager.DockAreaHasAutoHideButton, True)
# CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideShowOnMouseOver, True)
CDockManager.setAutoHideConfigFlag(CDockManager.AutoHideTitleBarForceCloseBtn, True)

dockMgr = CDockManager(win)

dock1 = CDockWidget('simple dock')
dockMgr.addDockWidget(DockWidgetArea.LeftDockWidgetArea, dock1)
# dockMgr.addAutoHideDockWidget(SideBarLocation.SideBarLeft, dock1)

dock2 = _DockWidget('press me')

dock3 = CDockWidget('dock 3')
dock3.setFeature(CDockWidget.DockWidgetDeleteOnClose, True)
dockMgr.addDockWidget(DockWidgetArea.RightDockWidgetArea, dock3)

# dock4 = CDockWidget('dock 4')
# dockMgr.addDockWidget(DockWidgetArea.RightDockWidgetArea, dock4)

label1.clicked.connect(lambda: (dock1.toggleView(True), dockMgr.addDockWidget(DockWidgetArea.LeftDockWidgetArea, dock1)))
label2.clicked.connect(lambda: (dock2.toggleView(True), dockMgr.addDockWidget(DockWidgetArea.LeftDockWidgetArea, dock2)))

win.dockMgr = dockMgr

win.show()
dockContainer = dockMgr.addDockWidgetFloating(dock2)
dockContainer.resize(300, 200)
# dock2.activateWindow()

app.exec()
