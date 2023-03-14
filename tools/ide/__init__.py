import os, sys, platform, argparse
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPalette
from editor.common.logger import log, error
from editor.models.editor.editor_prefs import EditorPrefs
from editor.theme_manager import loadTheme, setupThemeWatcher
from editor.main_window import MainWindow


###################################################################
def enableStdout(enabled):
	if enabled:
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__
	else:
		devnull = open(os.devnull, 'w')
		sys.stdout = devnull
		sys.stderr = devnull

def setupBundleInfo():
	system = platform.system()
	if system == 'Windows':
		import ctypes
		appid = 'dear_editor'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

	elif system == 'Darwin':
		# required python package: pyobjc-framework-Cocoa
		from Foundation import NSBundle
		bundle = NSBundle.mainBundle()
		app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
		if app_info: app_info['CFBundleName'] = 'Dear'

		# from Foundation import NSUserDefaults
		# defaults = NSUserDefaults.standardUserDefaults()
		# defaults.setObject_forKey_(['en'], 'AppleLanguages')


###################################################################
class Ide(QApplication):
	def __init__(self, *args):
		super().__init__(*args)
		self.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.setWindowIcon(QIcon('logo.png'))
		self.setApplicationName('Dear Editor')
		self.aboutToQuit.connect(self.onAboutToQuit)
		EditorPrefs.connect(os.environ[ 'DEAR_PREFS_PATH' ])

	def setupPalette(self):
		self.palette = self.style().standardPalette()
		self.palette.setColor(QPalette.Highlight, '#4999FD')
		self.setPalette(self.palette)

	def raiseWindow(self, prj, theme):
		log('hello!')
		loadTheme(theme)
		setupThemeWatcher()

		win = MainWindow()
		win.setWindowTitle(f'prj_xmile - OpenGL - {self.applicationName()}')
		win.show()

		sys.exit(self.exec())

	def onAboutToQuit(self):
		EditorPrefs.close()
		log('bye!')


###################################################################
def description():
	return 'raise editor ide'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear ide', description = description())
	parser.add_argument('-p', '--prj', help='specify working prject path')
	parser.add_argument('--theme', help='specify ide editor theme', default='dark')
	parser.add_argument('--stdout', action=argparse.BooleanOptionalAction, help='enable standard output', default=True)
	parser.add_argument('--host', action='store_true', help='start with host mode', default=False)
	args = parser.parse_args(argv)

	# if not args.prj: return error('raise ide with failure: prj not specified!')

	setupBundleInfo()
	enableStdout(args.stdout)

	ide = Ide(argv)
	ide.setupPalette()
	ide.raiseWindow(args.prj, args.theme)

