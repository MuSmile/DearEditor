import os, sys, platform
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPalette
from editor.common import argparse
from editor.common.logger import log
from editor.theme_manager import loadTheme, setupThemeWatcher
from editor.editor_prefs import EditorPrefs
from editor.main_window import MainWindow

def setupProcess():
	system = platform.system()
	if system == 'Windows':
		import ctypes
		appid = 'dear_editor.0.1'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

	elif system == 'Darwin':
		# required:
		# pip3 install pyobjc-framework-Cocoa
		try:
			from Foundation import NSBundle
			bundle = NSBundle.mainBundle()
			if not bundle: return
			app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
			if app_info: app_info['CFBundleName'] = 'Dear'
		except ImportError:
			pass
		pass


class Ide(QApplication):
	def __init__(self, *args):
		super().__init__(*args)
		self.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.setWindowIcon(QIcon('logo.png'))
		self.setApplicationName('Dear Editor')
		self.aboutToQuit.connect(self.onAboutToQuit)
		EditorPrefs.connect(os.environ[ 'DE_PREFS_PATH' ])
		self.setupPalette()

	def setupPalette(self):
		self.palette = self.style().standardPalette()
		self.palette.setColor(QPalette.Highlight, '#4999FD')
		self.setPalette(self.palette)

	def raiseWindow(self, prj, theme):
		log('hello!')
		loadTheme(theme)
		setupThemeWatcher()

		win = MainWindow()
		win.setWindowTitle(f'prj_xmile - dx11 - {self.applicationName()}')
		win.show()

		sys.exit(self.exec())

	def onAboutToQuit(self):
		EditorPrefs.close()
		log('bye!')


def description():
	return 'raise editor ide'

def main( argv ):
	parser = argparse.ArgumentParser(prog = 'dear ide', description = description())
	parser.add_argument('-p', '--prj', help='specify working prject path')
	parser.add_argument('--theme', help='specify ide theme')
	parser.add_argument('--host', action='store_true', help='start with host mode', default=False)
	args = parser.parse_args(argv)

	setupProcess()

	prj = args.prj or 'none'
	theme = args.theme or 'dark'

	ide = Ide(argv)
	ide.raiseWindow(prj, theme)