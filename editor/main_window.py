from PySide6.QtWidgets import QMainWindow
from editor.widgets.menubar import createMenuBar
from editor.widgets.toolbar import createToolBar
from editor.widgets.statusbar import createMainStatusBar
from editor.view_manager import createDockManager, createDockView

import editor.views, extensions

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		
		self.setGeometry(1000, 300, 800, 600)

		self.setMenuBar(createMenuBar(self))
		self.addToolBar(createToolBar(self))
		self.setStatusBar(createMainStatusBar(self))

		self.setupEditorViews()
		self.setFocus()


	def setupEditorViews(self):
		dockManager = createDockManager(self)
		self.dockManager = dockManager

		dock1 = createDockView('Hierarchy')
		dock1.addIntoEditor('right')

		dock2 = createDockView('Project')
		dock2.addIntoEditor('center')

		dock3 = createDockView('Console')
		dock3.addIntoEditor('right')

		dock4 = createDockView('Scene')
		dock4.addIntoEditor('bottom')

		# # rootarea = showEditorView('opengl', 'left')
		# area1 = showEditorView('Imgui', 'left')
		# area2 = showEditorView('Project', 'right')
		# showEditorView('Inspector', 'bottom', area2)
		# showEditorViewTabTo('Console', 'Inspector')
		# showEditorViewTabTo('Hierarchy', 'Imgui')
		# showEditorViewTabTo('FsmGraph', 'Imgui')

		# setDockSplitterSizes(area2, [600, 600])
		# setDockSplitterSizes(area1, [600, 600])

		# setDockFocused('Hierarchy')


	def closeEvent(self, evt):
		for fw in self.dockManager.floatingWidgets(): fw.close()
		super().closeEvent(evt)