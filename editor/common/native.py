"""This module provides os native toolkit.

.. warning::
    Native module only support MacOS and Windows for now!
"""

import platform
from PySide6.QtCore import Qt

__sys__ = platform.system()

def setDarkAppearance():
	"""Enable system dark mode appearance.
	"""
	if __sys__ == 'Windows':
		# from ctypes import c_int, byref, windll
		# from ctypes.wintypes import HWND
		# from editor.common.util import getMainWindow
	
		# DwmSetWindowAttribute = windll.dwmapi.DwmSetWindowAttribute
		# value = 2
		# value = c_int(value)
		# hwnd = HWND(int(getMainWindow().winId()))
		# DwmSetWindowAttribute(hwnd, 20, byref(value), 4)
		pass

	elif __sys__ == 'Darwin':
		from Cocoa import NSApp, NSAppearance
		appearance = NSAppearance.appearanceNamed_('NSAppearanceNameVibrantDark')
		NSApp.setAppearance_(appearance)

def setLightAppearance():
	"""Enable system light mode appearance.
	"""
	if __sys__ == 'Windows':
		pass

	elif __sys__ == 'Darwin':
		from Cocoa import NSApp, NSAppearance
		appearance = NSAppearance.appearanceNamed_('NSAppearanceNameVibrantLight')
		NSApp.setAppearance_(appearance)


# def setDarkAppearanceForWindow(widget):
# 	if __sys__ == 'Windows':
# 		pass

# 	elif __sys__ == 'Darwin':
# 		from objc import objc_object
# 		from Cocoa import NSAppearance

# 		widget.setAttribute(Qt.WA_NativeWindow, True)
# 		view = objc_object(c_void_p = widget.winId())
# 		window = view.window()

# 		window.setTitlebarAppearsTransparent_(True)

# 		# from Foundation import NSColor
# 		# from Cocoa import NSFullSizeContentViewWindowMask
# 		# color = NSColor.colorWithCalibratedRed_green_blue_alpha_(.3, .3, .3, 1)
# 		# window.setBackgroundColor_(color)
# 		# window.setStyleMask_(window.styleMask() | NSFullSizeContentViewWindowMask)
		
# 		appearance = NSAppearance.appearanceNamed_('NSAppearanceNameVibrantDark')
# 		window.setAppearance_(appearance)

# def setLightAppearanceForWindow(widget):
# 	if __sys__ == 'Windows':
# 		pass

# 	elif __sys__ == 'Darwin':
# 		from objc import objc_object
# 		from Cocoa import NSAppearance

# 		widget.setAttribute(Qt.WA_NativeWindow, True)
# 		view = objc_object(c_void_p = widget.winId())
# 		window = view.window()

# 		window.setTitlebarAppearsTransparent_(True)
# 		appearance = NSAppearance.appearanceNamed_('NSAppearanceNameVibrantLight')
# 		window.setAppearance_(appearance)

