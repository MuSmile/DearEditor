import sys, os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# from editor.tools.testkit import *
# from editor.widgets.menubar import *
# from editor.widgets.screenshot import *
# from editor.widgets.dropdown import *
# from editor.widgets.new_tree import *
from editor.widgets.toolbar import *
from editor.widgets.statusbar import *
from editor.widgets.preview import *
# from editor.widgets.color_picker import *
from editor.view_manager import createDockManager, DockView
# from editor.ide_globals import _G

import editor.views

# @addMenuItem('File/Restart', 55, 'Ctrl+R')
def _restart_program():
    python = sys.executable
    os.execl( python, python, *sys.argv )

class MainWindow(QMainWindow):
    closed = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        # _G.mainWindow = self
        # self.setupMenuBar()
        self.setupToolBar()
        self.setupStatusBar()
        self.setupEditorViews()
        self.setGeometry(1000, 300, 800, 600)
        self.setFocus()

    def setupToolBar(self):
        toolbar = createMainToolBar(self)
        self.addToolBar(toolbar)

    def setupStatusBar(self):
        statusbar = createMainStatusBar(self)
        self.setStatusBar(statusbar)

    # def closeEvent(self, evt):
    #     self.closed.emit()
    #     super().closeEvent(evt)
    #     for fw in self.dockManager.floatingWidgets(): fw.close()

    # def changeEvent(self, evt):
    #     super().changeEvent(evt)
    #     if evt.type() != QEvent.WindowStateChange: return
    #     if self.windowState() & Qt.WindowMinimized:
    #         self.maximizedSubwins = []
    #         for fwin in self.dockManager.floatingWidgets():
    #             if fwin.windowState() & Qt.WindowMaximized:
    #                 self.maximizedSubwins.append(fwin)
    #     elif evt.oldState() & Qt.WindowMinimized:
    #         if len(self.maximizedSubwins) == 0:
    #             del self.maximizedSubwins
    #         else:
    #             def restoreSubwins():
    #                 for swin in self.maximizedSubwins:
    #                     swin.showMaximized()
    #                     swin.setWindowOpacity(1)
    #                 del self.maximizedSubwins
    #             for swin in self.maximizedSubwins:
    #                 swin.setWindowOpacity(0)
    #             QTimer.singleShot(1, restoreSubwins)

    # def setupMenuBar(self):
    #     registerMenuItem('File/Exit', self.close, 99, shortcut = 'Ctrl+Q')
    #     registerMenuItem('File/Toggle', self.toggleStatusBar, 50, shortcut = 'Ctrl+T', checkable = True )

    #     registerMenuItem('Test/Save layout', self.saveLayout, 100, 'Ctrl+S')
    #     registerMenuItem('Test/Load layout', self.loadLayout, 101, 'Ctrl+L')

    #     registerMenuItem('Test/New dock', self.newDock, 150, 'Ctrl+N')
    #     registerMenuItem('Test/Aniamtor', lambda: showEditorView('Animator', 'bottom'), 151, 'A,S')
    #     registerMenuItem('Test/Take screenshot', takeScreenshot, 152, 'F10')
    #     registerMenuItem('Test/Test ColorPicker', lambda: createColorPicker('#8844aadd'), 154, 'C')
    #     registerMenuItem('Test/Test Runner', showTestRunner, 155, '`')

    #     # def dump():
    #     #     print(self.dockManager.perspectiveNames())
    #     # registerMenuItem('Dock/Dump', dump, 220, 'Ctrl+D')

    #     registerMenuItem('Dock/Toast', lambda:getEditorView('Project').showNotification('hello world', 1), 221, 'Ctrl+F')
    #     registerMenuItem('Dock/Toast2', lambda:getEditorView('FsmGraph').showNotification('hello world'), 222, 'Ctrl+G')
    #     registerMenuItem('Dock/Close focused', closeDockFocused, 223, 'Ctrl+W')
    #     # registerMenuItem('Dock/test', lambda: self.root.setAsCurrentTab(), 221, 'Ctrl+A')

    #     menubar = createMainMenuBar(self)
    #     # menubar.setNativeMenuBar(False)
    #     self.setMenuBar(menubar)

    # def toggleStatusBar(self, state):
    #     self.statusBar().setVisible(state)

    # def saveLayout(self):
    #     saveLayout('test')

    # def loadLayout(self):
    #     loadLayout('test')

    # def newDock(self):
    #     view = createEditorViewInstance('Hierarchy', 'Hierarchy -t')
    #     addViewTabTo(view, 'Imgui')

    def setupEditorViews(self):
        dockManager = createDockManager(self)
        self.dockManager = dockManager

        dock1 = DockView(dockManager, 'dock1')
        dock1.addIntoEditor('right')

        dock2 = DockView(dockManager, 'dock2')
        dock2.addIntoEditor('center')

        dock3 = DockView(dockManager, 'dock3')
        dock3.addIntoEditor('right')

        dock4 = DockView(dockManager, 'dock4')
        dock4.addIntoEditor('bottom')

        dock5 = DockView(dockManager, 'preview')
        dock5.setWidget(PreviewWidget())
        dock5.resize(500, 800)
        dock5.addIntoEditorAsFloating()

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
