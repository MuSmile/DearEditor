from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
# from editor.tools.testkit import *
# from editor.widgets.menubar import *
# from editor.widgets.screenshot import *
# from editor.widgets.dropdown import *
# from editor.widgets.new_tree import *
from editor.widgets.menubar import createMenuBar, menuItem
from editor.widgets.toolbar import *
from editor.widgets.statusbar import *
# from editor.widgets.color_picker import *
from editor.view_manager import createDockManager, DockView
# from editor.ide_globals import _G


import numpy as np
from OpenGL import GL as gl
from PySide6.QtOpenGL import *
from PySide6.QtOpenGLWidgets import *
class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Triangle, PyQt5, OpenGL ES 2.0")
        self.resize(300, 300)
    def initializeGL(self):
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        vertShaderSrc = """
            attribute vec3 aPosition;
            void main()
            {
                gl_Position = vec4(aPosition, 1.0);
            }
        """
        fragShaderSrc = """
            void main()
            {
                gl_FragColor = vec4(0.8, 0.6, 0.4, 1.0);
            }
        """
        program = QOpenGLShaderProgram(self)
        program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertShaderSrc)
        program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragShaderSrc)
        program.link()
        program.bind()
        vertPositions = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0], dtype=np.float32)
        self.vertPosBuffer = QOpenGLBuffer()
        self.vertPosBuffer.create()
        self.vertPosBuffer.bind()
        self.vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)
        program.bindAttributeLocation("aPosition", 0)
        program.setAttributeBuffer(0, gl.GL_FLOAT, 0, 3)
        program.enableAttributeArray(0)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)


import editor.views
class MyPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.Popup, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowOpacity(0.1)
        # self.setStyleSheet('QWidget { background-color: transparent; }')
        self.btn = QPushButton('test', self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn.resize(self.width(), self.height())


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.setGeometry(1000, 300, 800, 600)
        
        self.setMenuBar(createMenuBar(self))
        self.addToolBar(createToolBar(self))
        self.setStatusBar(createMainStatusBar(self))

        self.setupEditorViews()
        self.setFocus()


    def closeEvent(self, evt):
        for fw in self.dockManager.floatingWidgets(): fw.close()
        super().closeEvent(evt)

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

    # def saveLayout(self):
    #     saveLayout('test')

    # def loadLayout(self):
    #     loadLayout('test')

    def setupEditorViews(self):
        dockManager = createDockManager(self)
        self.dockManager = dockManager

        dock1 = DockView(dockManager, 'dock1')
        dock1.addIntoEditor('right')

        dock2 = DockView(dockManager, 'dock2', 'project.png')
        dock2.addIntoEditor('center')

        dock3 = DockView(dockManager, 'dock3', 'console.png')
        dock3.addIntoEditor('right')

        dock4 = DockView(dockManager, 'opengl dock', 'inspector.png')
        dock4.addIntoEditor('bottom')
        dock4.setWidget(OpenGLWidget(dock4))

        from editor.widgets.complex.tree_view import runTreeDemo
        self.btn = QPushButton("Click me")
        self.btn.setGeometry(QRect(0, 0, 100, 30))
        # self.btn.clicked.connect(self.doit)
        self.btn.clicked.connect(runTreeDemo)
        dock2.setWidget(self.btn)

    def doit(self):
        self.w = MyPopup()
        self.w.show()
        self.w.resize(200, 300)
        self.w.move(QCursor.pos())

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
