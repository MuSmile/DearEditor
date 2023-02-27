import numpy as np
from OpenGL import GL as gl
from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from editor.view_manager import DockView, dockView

class OpenGLWidget(QOpenGLWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setWindowTitle("Triangle, PyQt5, OpenGL ES 2.0")
		self.resize(300, 300)
	def initializeGL(self):
		gl.glClearColor(0.3, 0.3, 0.3, 1.0)
		vertShaderSrc = '''
			attribute vec3 aPosition;
			void main()
			{
				gl_Position = vec4(aPosition, 1.0);
			}
		'''
		fragShaderSrc = '''
			void main()
			{
				gl_FragColor = vec4(0.8, 0.6, 0.4, 1.0);
			}
		'''
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


@dockView('Scene', icon = 'scene.png', title = 'OpenGL Test')
class SceneView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)
		self.setWidget(OpenGLWidget(self))

