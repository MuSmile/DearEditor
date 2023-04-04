from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.common.util import smartString
from editor.models.editor.data_grid import PropertyGroup


_datagridRegistry = {}
def registerPropertyCreator(type, func):
	if type in _datagridRegistry: warn(f'Property creator for \'{type}\' has registered!')
	_datagridRegistry[ type ] = func
def propertyCreator(type):
	def warpper(func):
		registerPropertyCreator(type, func)
		return func
	return warpper

def registerPropertyGroup(type, cls):
	if type in _datagridRegistry: warn(f'Property group class \'{cls}\' has registered!')
	_datagridRegistry[ type ] = cls
def propertyGroup(type):
	def wrapper(cls):
		registerPropertyGroup(type, cls)
		return cls
	return wrapper

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
	label.setToolTip(property.label())
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

@propertyGroup('box_group')
class BoxGroup(QWidget):
	@Property(int)
	def borderRadius(self):
		return self._borderRadius
	@borderRadius.setter
	def borderRadius(self, value):
		self._borderRadius = value

	def __init__(self, group, parent = None):
		super().__init__(parent)
		self.group = group
		self._borderRadius = 2

		layout = DataGridLayout()
		layout.initLayout(group.properties)
		layout.setContentsMargins(0, 25, 0, 3)
		self.setLayout(layout)

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		rect = self.rect()
		path = QPainterPath()
		path.addRoundedRect(rect, self._borderRadius, self._borderRadius)
		painter.setClipPath(path)
		
		palette = self.palette()
		w, h = rect.width(), rect.height()
		painter.fillRect(QRect(0, 0, w, h), palette.color(QPalette.Base))
		painter.fillRect(QRect(0, 0, w, 22), QColor('#3a3a3a'))
		
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(QRect(6, 0, w, 22), Qt.AlignVCenter, smartString(self.group.name))

		option = QStyleOptionFrame()
		option.initFrom(self)
		option.frameShape = QFrame.StyledPanel
		self.style().drawPrimitive(QStyle.PE_Frame, option, painter, self)

@propertyGroup('title_group')
class TitleGroup(QWidget):
	def __init__(self, group, parent = None):
		super().__init__(parent)
		self.group = group
		layout = DataGridLayout()
		layout.initLayout(group.properties)
		layout.setContentsMargins(0, 28, 0, 3)
		self.setLayout(layout)

	def paintEvent(self, evt):
		super().paintEvent(evt)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.TextAntialiasing)

		palette = self.palette()
		w, h = self.width(), self.height()
		painter.setPen(palette.color(QPalette.Text))
		painter.drawText(QRect(6, 0, w, 22), Qt.AlignVCenter, smartString(self.group.name))
		painter.fillRect(QRect(6, 23, w - 9, 1), palette.color(QPalette.Base))
