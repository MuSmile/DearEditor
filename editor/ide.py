import sys, platform
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication
from editor.ide_prefs import IdePrefs
from editor.main_window import MainWindow
from editor.theme_manager import loadTheme, setupThemeWatcher
from editor.common.logger import log


def _init_platform(system):
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
		_init_platform(platform.system())
		super().__init__(*args)
		self.setAttribute(Qt.AA_EnableHighDpiScaling)
		self.setWindowIcon(QIcon('logo.png'))
		self.setApplicationName('Dear Editor')
		self.aboutToQuit.connect(self.onAboutToQuit)
		IdePrefs.connect('prefs.db')

	def raiseWindow(self, prj):
		log('hello!')
		loadTheme('dark')
		setupThemeWatcher()

		win = MainWindow()
		win.setWindowTitle(f'prj_xmile - dx11 - {self.applicationName()}')
		win.show()

		sys.exit(self.exec())

	def onAboutToQuit(self):
		IdePrefs.close()
		log('bye!')
