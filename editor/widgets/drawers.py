"""This module provides drawer support for Property and PropertyGroup.
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.common.util import smartString

_drawerRegistry = {}
def registerDrawerCreator(type, func):
	if type in _drawerRegistry: warn(f'Drawer creator for \'{type}\' has registered!')
	_drawerRegistry[ type ] = func
def drawerCreator(type):
	def warpper(func):
		registerPropertyCreator(type, func)
		return func
	return warpper


def createPropertyLabel(property, parent):
	creator = _drawerRegistry[ property.type ]
	return creator(property, parent)

def createPropertyDrawer(property, parent):
	creator = _drawerRegistry[ property.type ]
	return creator(property, parent)

def createGroupDrawer(group, parent):
	creator = _drawerRegistry[ group.type ]
	return creator(group, parent)

