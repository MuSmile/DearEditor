"""This module provides drawer support for Property and PropertyGroup.
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.common.logger import warn
from editor.common.util import smartString
from editor.models.editor.property_model import PropertyGroup, PropertyType, GroupType


_drawerRegistry = {}
def registerDrawerCreator(type, func):
	if type in _drawerRegistry: warn(f'Drawer creator for \'{type}\' has registered!')
	_drawerRegistry[ type ] = func
def drawerCreator(type):
	def warpper(func):
		registerDrawerCreator(type, func)
		return func
	return warpper

def createPropertyLabel(property, parent = None):
	label = smartString(property.label())
	return QLabel(label, parent)

def createPropertyDrawer(property, parent = None):
	creator = _drawerRegistry[ property.type ]
	return creator(property, parent)

def createGroupDrawer(group, parent = None):
	creator = _drawerRegistry[ group.type ]
	return creator(group, parent)


##################################################
class DataGridLayout(QGridLayout):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setContentsMargins(0, 0, 0, 0)
		self.setHorizontalSpacing(0)
		self.setVerticalSpacing(3)
		self.setColumnMinimumWidth(0, 120)
		self.setColumnStretches(1, 2)
		self.setAlignment(Qt.AlignTop)
		self._groupSpacing = 10

	def _addPropertyInternal(self, curr, prev = None):
		currIsGroup = isinstance(curr, PropertyGroup)
		prevIsGroup = isinstance(prev, PropertyGroup)
		needSpace = currIsGroup or prevIsGroup
		if isinstance(curr, PropertyGroup):
			if needSpace: self.addSpace(self._groupSpacing, 'group_space')
			self.addPropertyGroup(curr)
		else:
			if needSpace: self.addSpace(self._groupSpacing, 'group_space')
			self.addProperty(curr)
		# link setColumnStretches

	def initLayout(self, properties):
		count = len(properties)
		if count == 0: return
		self._addPropertyInternal(properties[ 0 ])
		for i in range(1, count):
			curr = properties[ i ]
			prev = properties[ i - 1 ]
			self._addPropertyInternal(curr, prev)

	def setColumnStretches(self, col0, col1):
		self.setColumnStretch(0, col0)
		self.setColumnStretch(1, col1)

	def addRow(self, label, field):
		count = self.rowCount()
		label.setObjectName('datagrid-label')
		field.setObjectName('datagrid-field')
		self.addWidget(label, count, 0)
		self.addWidget(field, count, 1)

	def addRowSpan(self, widget):
		count = self.rowCount()
		widget.setObjectName('datagrid-span')
		self.addWidget(widget, count, 0, 1, 2)

	def addProperty(self, property):
		parent = self.parent()
		label = createPropertyLabel(property, parent)
		drawer = createPropertyDrawer(property, parent)
		self.addRow(label, drawer)

	def addPropertyGroup(self, group):
		wgt = createGroupDrawer(group, self.parent())
		self.addRowSpan(wgt)

	def addSpace(self, space, name = None):
		wgt = QWidget()
		wgt.setFixedHeight(space)
		self.addRowSpan(wgt)
		if name: wgt.setObjectName(name)

class DataGridView(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setLayout(DataGridLayout())
		self.model = None

	def clearLayout(self):
		layout = self.layout()
		while True:
			item = layout.takeAt(0)
			if item: item.deleteLater()
			else: break
		self.model = None

	def setPropertyModel(self, model):
		if self.model: self.clearLayout()
		self.layout().initLayout(model.properties)
		self.model = model


##################################################
from editor.widgets.basic.line_edit import LineEdit, IntLineEdit, PathLineEdit
from editor.widgets.basic.color_edit import ColorEdit
from editor.widgets.basic.object_edit import ObjectEdit
from editor.widgets.group.title_group import TitleGroup
from editor.widgets.group.box_group import BoxGroup

@drawerCreator(PropertyType.Int)
def _createIntDrawer(property, parent):
	# label.setToolTip(property.label())
	drawer = IntLineEdit()
	drawer.setFocusPolicy(Qt.StrongFocus)
	return drawer

@drawerCreator(PropertyType.Float)
def _createFloatDrawer(property, parent):
	drawer = QSlider(Qt.Horizontal)
	drawer.setFocusPolicy(Qt.StrongFocus)
	return drawer

@drawerCreator(PropertyType.String)
def _createStringDrawer(property, parent):
	drawer = LineEdit()
	drawer.setFocusPolicy(Qt.StrongFocus)
	return drawer

@drawerCreator(PropertyType.Color)
def _createColorDrawer(property, parent):
	drawer = ColorEdit()
	drawer.setFocusPolicy(Qt.StrongFocus)
	return drawer

@drawerCreator(PropertyType.Object)
def _createObjectDrawer(property, parent):
	drawer = ObjectEdit()
	drawer.setFocusPolicy(Qt.StrongFocus)
	return drawer
# 
@drawerCreator('path')
# def _createPathDrawer(property, parent):
# 	drawer = PathLineEdit(True)
# 	drawer.setFocusPolicy(Qt.StrongFocus)
# 	return drawer

@drawerCreator(GroupType.TitleGroup)
def _createTitleGroupDrawer(group, parent):
	layout = DataGridLayout()
	layout.initLayout(group.properties)
	group = TitleGroup(smartString(group.name), layout)
	group.setHorizontalMargins(6, 4)
	return group

@drawerCreator(GroupType.BoxGroup)
def _createBoxGroupDrawer(group, parent):
	layout = DataGridLayout()
	layout.initLayout(group.properties)
	group = BoxGroup(smartString(group.name), layout)
	return group
