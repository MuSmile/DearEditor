from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.common.util import smartString
from editor.models.editor.data_grid import PropertyGroup
from editor.widgets.group.title_group import TitleGroup
from editor.widgets.group.box_group import BoxGroup


_datagridRegistry = {}
def registerPropertyCreator(type, func):
	if type in _datagridRegistry: warn(f'Property creator for \'{type}\' has registered!')
	_datagridRegistry[ type ] = func
def propertyCreator(type):
	def warpper(func):
		registerPropertyCreator(type, func)
		return func
	return warpper

def createPropertyWidget(property):
	return _datagridRegistry[ property.type ](property)

def createPropertyGroupWidget(group, parent):
	return _datagridRegistry[ group.type ](group, parent)


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
		label, field = createPropertyWidget(property)
		self.addRow(label, field)

	def addPropertyGroup(self, group):
		wgt = createPropertyGroupWidget(group, self.parent())
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
		self.datagrid = None

	def clearLayout(self):
		layout = self.layout()
		while True:
			item = layout.takeAt(0)
			if item: item.deleteLater()
			else: break
		self.datagrid = None

	def setDataGrid(self, datagrid):
		if self.datagrid: self.clearLayout()
		self.layout().initLayout(datagrid.properties)
		self.datagrid = datagrid


##################################################
from editor.widgets.basic.line_edit import LineEdit, IntLineEdit, PathLineEdit
from editor.widgets.basic.color_edit import ColorEdit
from editor.widgets.basic.reference_edit import ReferenceEdit

@propertyCreator('int')
def _createPropertyWidgetInt(property):
	label = QLabel(smartString(property.label()))
	# label.setToolTip(property.label())
	editor = IntLineEdit()
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor
@propertyCreator('float')
def _createPropertyWidgetFloat(property):
	label = QLabel(smartString(property.label()))
	editor = QSlider(Qt.Horizontal)
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor
@propertyCreator('string')
def _createPropertyWidgetFloat(property):
	label = QLabel(smartString(property.label()))
	editor = LineEdit()
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor
@propertyCreator('color')
def _createPropertyWidgetFloat(property):
	label = QLabel(smartString(property.label()))
	editor = ColorEdit()
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor
@propertyCreator('reference')
def _createPropertyWidgetFloat(property):
	label = QLabel(smartString(property.label()))
	editor = ReferenceEdit()
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor
@propertyCreator('path')
def _createPropertyWidgetFloat(property):
	label = QLabel(smartString(property.label()))
	editor = PathLineEdit(True)
	editor.setFocusPolicy(Qt.StrongFocus)
	return label, editor

@propertyCreator('title_group')
def _createPropertyWidgetFloat(group, parent):
	layout = DataGridLayout()
	layout.initLayout(group.properties)
	group = TitleGroup(smartString(group.name), layout)
	group.setHorizontalMargins(6, 4)
	return group
@propertyCreator('box_group')
def _createPropertyWidgetFloat(group, parent):
	layout = DataGridLayout()
	layout.initLayout(group.properties)
	group = BoxGroup(smartString(group.name), layout)
	return group
