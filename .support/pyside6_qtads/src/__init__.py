# try below if meet lib path issues

# import os, site
# _pkg_dir = next(p for p in site.getsitepackages() if p.endswith(('site-packages')))
# os.add_dll_directory(_pkg_dir + '/PySide6')
# os.add_dll_directory(_pkg_dir + '/shiboken6')

# from PySide6.QtWidgets import QApplication
# _plugin_dir = _pkg_dir + '/PySide6/plugins'

# def _checkPluginDir():
# 	for path in QApplication.libraryPaths():
# 		if os.path.samefile(path, _plugin_dir):
# 			return True
# 	return False

# if not _checkPluginDir():
# 	print('PySide plugins dir not found! trying resolve ...')
# 	QApplication.addLibraryPath(_plugin_dir)
# 	# set env var: QT_PLUGIN_PATH = C:\Users{YOUR_USERNAME}\Anaconda3\Library\plugins


####################### qtads #######################
import os

_cwd = os.getcwd()
os.chdir(os.path.dirname(__file__))
from .PySide6QtAds import ads
os.chdir(_cwd)

CDockWidget               =   ads.CDockWidget
CDockManager              =   ads.CDockManager
DockWidgetArea            =   ads.DockWidgetArea
SideBarLocation           =   ads.SideBarLocation
TitleBarButton            =   ads.TitleBarButton


####################### export #######################
__all__ = [
	'CDockWidget'            ,
	'CDockManager'           ,
	'DockWidgetArea'         ,
	'SideBarLocation'        ,
	'TitleBarButton'         ,
]
