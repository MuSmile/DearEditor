import platform
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtWidgets import QMainWindow
from editor.widgets.menubar import createMenuBar
from editor.widgets.toolbar import createToolBar
from editor.widgets.statusbar import createStatusBar
from editor.view_manager import createDockManager, createDockView
from editor.common.util import getIde
import editor.views, extensions

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		
		self.setGeometry(1000, 300, 800, 600)

		self.setMenuBar(createMenuBar(self))
		self.addToolBar(createToolBar(self))
		self.setStatusBar(createStatusBar(self))

		self.setupEditorViews()
		self.activateWindow()


	def setupEditorViews(self):
		self.dockMgr = createDockManager(self)

		dock1 = createDockView('Hierarchy')
		dock1.addIntoEditor('right')

		dock2 = createDockView('Gallery')
		dock2.addIntoEditor()

		dock3 = createDockView('Project')
		dock3.addIntoEditor('right')

		dock4 = createDockView('Scene')
		dock4.addIntoEditor('bottom')


	def changeEvent(self, evt):
		super().changeEvent(evt)

		if evt.type() != QEvent.WindowStateChange: return
		if platform.system() != 'Windows': return

		if self.windowState() & Qt.WindowMinimized:
			self.maximizedFloatings = []
			for f in self.dockMgr.floatingWidgets():
				if f.windowState() & Qt.WindowMaximized:
					self.maximizedFloatings.append(f)
		
		elif evt.oldState() & Qt.WindowMinimized:
			if not self.maximizedFloatings: return
			def restoreFloatings():
				for f in self.maximizedFloatings:
					f.showMaximized()
					f.setWindowOpacity(1)
				self.maximizedFloatings = []
				self.activateWindow()

			for f in self.maximizedFloatings: f.setWindowOpacity(0)
			QTimer.singleShot(1, restoreFloatings)


	def closeEvent(self, evt):
		for w in getIde().topLevelWidgets(): w.close()
		super().closeEvent(evt)

