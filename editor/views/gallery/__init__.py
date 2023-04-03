from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.complex.tree_stacked import TreeStackedWidget
from editor.models.editor.data_grid import DataGrid
from editor.widgets.complex.datagrid_view import DataGridView
from editor.widgets.complex.sliding_stacked import SlidingStackedWidget
from editor.widgets.basic.range_slider import RangeSlider
from editor.widgets.basic.progress_bar import ProgressBar
from editor.widgets.basic.line_edit import LineEdit, IntLineEdit, FloatLineEdit, SearchLineEdit, PlaceholderLineEdit, PathLineEdit
from editor.widgets.basic.drop_down import DropDown, FlagDropDown
from editor.widgets.basic.text_area import TextArea
from editor.widgets.basic.color_edit import ColorEdit
from editor.widgets.basic.reference_edit import ReferenceEdit
from editor.widgets.basic.spinner import WaitingSpinner
from editor.widgets.misc.collapsible import CollapsibleWidget
from editor.widgets.misc.line import HLineWidget
from editor.common.icon_cache import getThemeIcon, getThemePixmap
from editor.common.util import createTestMenu
from editor.view_manager import DockView, dockView


@dockView('Gallery')
class GalleryView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)

		layout = QVBoxLayout()
		self.layout().addLayout(layout)

		searchbar = QWidget(self)
		searchbar.setFixedHeight(24)
		searchbar.setObjectName('searchbar')
		searchbarLayout = QHBoxLayout(searchbar)
		searchbarLayout.setContentsMargins(0, 2, 2, 4)
		searchbarLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout.addWidget(searchbar)

		searchEdit = SearchLineEdit(self)
		searchEdit.setFixedWidth(300)
		searchbarLayout.addWidget(searchEdit)

		treeStacked = TreeStackedWidget(self)
		treeStacked.addStackedWidget('Basic/Button', self.createButtonPreview())
		treeStacked.addStackedWidget('Basic/LineEdit', self.createLineEditPreview())
		treeStacked.addStackedWidget('Basic/TextArea', self.createTextAreaPreview())
		treeStacked.addStackedWidget('Basic/Slider', self.createSliderPreview())
		treeStacked.addStackedWidget('Basic/Spinner', self.createSpinnerPreview())
		treeStacked.addStackedWidget('Basic/Vector', None)
		treeStacked.addStackedWidget('Group/SimpleGroup', None)
		treeStacked.addStackedWidget('Group/TitleGroup', None)
		treeStacked.addStackedWidget('Group/BoxGroup', None)
		treeStacked.addStackedWidget('Group/FoldoutGroup', None)
		treeStacked.addStackedWidget('Group/ToggleGroup', None)
		treeStacked.addStackedWidget('Group/TabGroup', None)
		treeStacked.addStackedWidget('Complex/SlidingStacked', self.createSlidingStackedPreview())
		treeStacked.addStackedWidget('Complex/CurveEditor', None)
		treeStacked.addStackedWidget('Complex/ListDrawer', None)
		treeStacked.addStackedWidget('Complex/DictDrawer', None)
		treeStacked.addStackedWidget('Complex/DataGrid', self.createDataGridPreview())
		treeStacked.addStackedWidget('Misc/Collapsible', self.createCollapsiblePreview())
		treeStacked.addStackedWidget('Misc/InfoBox', None)
		treeStacked.addStackedWidget('Misc/Palette', None)
		treeStacked.addStackedWidget('Misc/Toast', None)
		treeStacked.tree.setCurrentByPath('Basic/Button')
		treeStacked.tree.expandAll()
		layout.addWidget(treeStacked)

	def createButtonPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  PUSHBUTTON  #############
		layout.addWidget(QLabel('PushButton'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		pushBtnLayout = QHBoxLayout()
		pushBtnLayout.setAlignment(Qt.AlignLeft)
		# pushBtnLayout.setSpacing(5)

		pushBtn1 = QPushButton('normal')
		pushBtn2 = QPushButton(getThemeIcon('project.png'), 'icon')
		pushBtn3 = QPushButton('popup')
		pushBtn3.setMenu(createTestMenu(pushBtn3))

		pushBtn4 = QPushButton(getThemeIcon('project.png'), 'all')
		pushBtn4.setMenu(createTestMenu(pushBtn4))
		pushBtn4.setFixedWidth(100)
		pushBtn5 = QPushButton('checkable')
		pushBtn5.setCheckable(True)
		pushBtn5.setChecked(True)

		pushBtn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		pushBtn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		pushBtn3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		pushBtn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		pushBtn5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		pushBtnLayout.addWidget(pushBtn1)
		pushBtnLayout.addWidget(pushBtn2)
		pushBtnLayout.addWidget(pushBtn3)
		pushBtnLayout.addWidget(pushBtn4)
		pushBtnLayout.addWidget(pushBtn5)
		layout.addLayout(pushBtnLayout)


		#############  TOOLBUTTON  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ToolButton'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		toolBtnLayout = QHBoxLayout()
		toolBtnLayout.setAlignment(Qt.AlignLeft)

		toolBtn1 = QToolButton()
		toolBtn1.setIcon(getThemeIcon('project.png'))
		toolBtn2 = QToolButton()
		toolBtn2.setIcon(getThemeIcon('project.png'))
		toolBtn2.setCheckable(True)
		toolBtn2.setChecked(True)
		toolBtn3 = QToolButton()
		toolBtn3.setIcon(getThemeIcon('project.png'))
		toolBtn3.setPopupMode(QToolButton.MenuButtonPopup)
		toolBtn3.setMenu(createTestMenu(toolBtn3))
		toolBtn4 = QToolButton()
		toolBtn4.setIcon(getThemeIcon('project.png'))
		toolBtn4.setPopupMode(QToolButton.InstantPopup)
		toolBtn4.setMenu(createTestMenu(toolBtn4))
		toolBtn5 = QToolButton()
		toolBtn5.setText('popup')
		toolBtn5.setPopupMode(QToolButton.InstantPopup)
		toolBtn5.setMenu(createTestMenu(toolBtn5))
		toolBtn6 = QToolButton()
		toolBtn6.setText('popup')
		toolBtn6.setPopupMode(QToolButton.MenuButtonPopup)
		toolBtn6.setMenu(createTestMenu(toolBtn6))
		toolBtn7 = QToolButton()
		toolBtn7.setText('checkable')
		toolBtn7.setCheckable(True)
		toolBtn7.setChecked(True)

		toolBtn1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		toolBtn2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		toolBtn3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		toolBtn4.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		toolBtn5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		toolBtn6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		toolBtn7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		toolBtnLayout.addWidget(toolBtn1)
		toolBtnLayout.addWidget(toolBtn2)
		toolBtnLayout.addWidget(toolBtn3)
		toolBtnLayout.addWidget(toolBtn4)
		toolBtnLayout.addWidget(toolBtn5)
		toolBtnLayout.addWidget(toolBtn6)
		toolBtnLayout.addWidget(toolBtn7)
		layout.addLayout(toolBtnLayout)


		#############  DROPDOWN  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('DropDown'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		dropDownLayout = QHBoxLayout()
		dropDownLayout.setSpacing(20)
		dropDownLayout.setAlignment(Qt.AlignLeft)

		dropdown1 = DropDown()
		dropdown1.setItems(['Zero', 'One', 'Two', 'Three'])
		dropdown1.setCurrentIndex(2)
		dropdown1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		dropdown1.setFocusPolicy(Qt.StrongFocus)

		dropdown2 = DropDown()
		dropdown2.setItems([f'Item {x}' for x in range(40)])
		dropdown2.setCurrentIndex(3)
		dropdown2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		dropDownLayout.addWidget(dropdown1)
		dropDownLayout.addWidget(dropdown2)
		layout.addLayout(dropDownLayout)


		layout.addSpacing(20)
		layout.addWidget(QLabel('FlagDropDown'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		flagLayout = QHBoxLayout()
		flagLayout.setSpacing(20)
		flagLayout.setAlignment(Qt.AlignLeft)

		flag1 = FlagDropDown()
		flag1.setItems(['Zero', 'One', 'Two', 'Three'])
		flag1.setCurrentIndex(2)
		flag1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		flag1.setFocusPolicy(Qt.StrongFocus)

		flag2 = FlagDropDown()
		flag2.setItems([f'Item {x}' for x in range(40)])
		flag2.setCurrentIndex(127)
		flag2.setFlag('Item 0', False)
		flag2.setCurrentIndex(0)
		QTimer.singleShot(111, lambda:flag2.setCurrentIndex(0))
		flag2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		flagLayout.addWidget(flag1)
		flagLayout.addWidget(flag2)
		layout.addLayout(flagLayout)


		#############  CHECKBOX  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('CheckBox/RadioButton'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		checkBoxLayout = QHBoxLayout()
		checkBoxLayout.setSpacing(20)
		checkBoxLayout.setAlignment(Qt.AlignLeft)

		checkBox1 = QCheckBox('normal')
		checkBox1.setFocusPolicy(Qt.StrongFocus)
		checkBox2 = QCheckBox('icon')
		checkBox2.setTristate(True)
		checkBox2.setIcon(getThemeIcon('project.png'))
		checkBox2.setFocusPolicy(Qt.StrongFocus)
		checkBox3 = QCheckBox()
		checkBox3.setFocusPolicy(Qt.StrongFocus)

		radioBtn1 = QRadioButton('normal')
		radioBtn1.setFocusPolicy(Qt.StrongFocus)
		radioBtn2 = QRadioButton('icon')
		radioBtn2.setIcon(getThemeIcon('project.png'))
		radioBtn2.setFocusPolicy(Qt.StrongFocus)

		checkBoxLayout.addWidget(checkBox1)
		checkBoxLayout.addWidget(checkBox2)
		checkBoxLayout.addWidget(checkBox3)

		checkBoxLayout.addWidget(radioBtn1)
		checkBoxLayout.addWidget(radioBtn2)
		layout.addLayout(checkBoxLayout)


		return preview
	def createLineEditPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  LINEEDIT  #############
		layout.addWidget(QLabel('LineEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		lineEditLayout = QHBoxLayout()
		lineEditLayout.setSpacing(20)
		lineEditLayout.setAlignment(Qt.AlignLeft)

		lineEdit1 = LineEdit()
		lineEdit1.setClearButtonEnabled(True)
		lineEdit2 = PlaceholderLineEdit('placeholder')

		lineEditLayout.addWidget(lineEdit1)
		lineEditLayout.addWidget(lineEdit2)
		layout.addLayout(lineEditLayout)


		#############  LINEEDIT  #############
		layout.addWidget(QLabel('NumberEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		numberEditLayout = QHBoxLayout()
		numberEditLayout.setSpacing(20)
		numberEditLayout.setAlignment(Qt.AlignLeft)

		intEdit = IntLineEdit()
		floatEdit = FloatLineEdit()

		numberEditLayout.addWidget(intEdit)
		numberEditLayout.addWidget(floatEdit)
		layout.addLayout(numberEditLayout)


		#############  SEARCH  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('SearchEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		searchEditLayout = QHBoxLayout()
		searchEditLayout.setSpacing(20)
		searchEditLayout.setAlignment(Qt.AlignLeft)

		searchEdit = SearchLineEdit()

		searchEditLayout.addWidget(searchEdit)
		layout.addLayout(searchEditLayout)


		#############  PATH  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('PathEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		pathEditLayout = QHBoxLayout()
		pathEditLayout.setSpacing(20)
		pathEditLayout.setAlignment(Qt.AlignLeft)

		filePathEdit = PathLineEdit(False)
		folderPathEdit = PathLineEdit(True)

		pathEditLayout.addWidget(filePathEdit)
		pathEditLayout.addWidget(folderPathEdit)
		layout.addLayout(pathEditLayout)


		#############  COLOR  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ColorEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		colorEditLayout = QHBoxLayout()
		colorEditLayout.setSpacing(20)
		colorEditLayout.setAlignment(Qt.AlignLeft)

		colorEdit = ColorEdit()

		colorEditLayout.addWidget(colorEdit)
		layout.addLayout(colorEditLayout)


		#############  REFERENCE  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ReferenceEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		referanceEditLayout = QHBoxLayout()
		referanceEditLayout.setSpacing(20)
		referanceEditLayout.setAlignment(Qt.AlignLeft)

		referanceEdit = ReferenceEdit()

		referanceEditLayout.addWidget(referanceEdit)
		layout.addLayout(referanceEditLayout)


		#############  KEYSEQ  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('KeySequenceEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		keySeqLayout = QHBoxLayout()
		keySeqLayout.setSpacing(20)
		keySeqLayout.setAlignment(Qt.AlignLeft)

		keySeq = QKeySequenceEdit()

		keySeqLayout.addWidget(keySeq)
		layout.addLayout(keySeqLayout)

		return preview
	def createTextAreaPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('TextArea'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		textLayout = QHBoxLayout()
		textLayout.setSpacing(50)
		textLayout.setAlignment(Qt.AlignTop)

		ws1 = TextArea()
		textLayout.addWidget(ws1)
		
		layout.addLayout(textLayout)


		return preview
	def createSliderPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('ProgressBar'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		comboBoxLayout = QHBoxLayout()
		comboBoxLayout.setSpacing(20)
		comboBoxLayout.setAlignment(Qt.AlignLeft)

		progressBar = ProgressBar()
		progressBar.setFixedWidth(200)
		# progressBar.setValue(30)
		progressBar2 = QProgressBar()
		progressBar2.setValue(30)


		comboBoxLayout.addWidget(progressBar)
		comboBoxLayout.addWidget(progressBar2)
		layout.addLayout(comboBoxLayout)


		#############  SLIDER  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('Slider'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		sliderLayout = QHBoxLayout()
		sliderLayout.setSpacing(20)
		sliderLayout.setAlignment(Qt.AlignLeft)

		slider1 = QSlider(Qt.Horizontal)
		slider1.setMinimum(0)
		slider1.setMaximum(100)
		slider1.setSingleStep(1)
		slider1.setFixedWidth(200)
		slider1.setValue(20)
		slider1.valueChanged.connect(lambda v: progressBar.setValue(v))
		slider1.setFocusPolicy(Qt.StrongFocus)
		# slider2 = RangeSlider(Qt.Horizontal)
		# slider2.setMinimumHeight(30)
		# slider2.setMinimum(0)
		# slider2.setMaximum(255)
		# slider2.setLow(15)
		# slider2.setHigh(35)
		# slider2.setTickPosition(QSlider.TicksBelow)
		# slider2.setFixedWidth(200)
		# slider2.setFocusPolicy(Qt.StrongFocus)

		slider3 = RangeSlider()
		# slider1.setMinimum(0)
		# slider1.setMaximum(100)
		# slider1.setSingleStep(1)
		# slider1.setValue(20)
		slider3.setFixedWidth(200)
		slider3.setFocusPolicy(Qt.StrongFocus)

		sliderLayout.addWidget(slider1)
		# sliderLayout.addWidget(slider2)
		sliderLayout.addWidget(slider3)
		layout.addLayout(sliderLayout)

		return preview
	def createCollapsiblePreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('Collapsible'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		btnGroup = QWidget()
		btnGroup.setObjectName('test')
		btnGroup.setStyleSheet('#test { background:#333; border-radius: 5px; }')
		btnLayout = QVBoxLayout()
		btnLayout.setSpacing(10)
		subLayout = QHBoxLayout()
		btnLayout.addLayout(subLayout)
		btnGroup.setLayout(btnLayout)
		for i in range(10): btnLayout.addWidget(QPushButton(f'Item {i}'))
		for i in range(4): subLayout.addWidget(QPushButton(f'Item {i}'))

		collapsible = CollapsibleWidget()
		collapsible.setWidget(btnGroup)
		collapsible.updateFixedHeight()
		
		btnLayout = QHBoxLayout()
		btn0 = QPushButton('Toggle')
		btn1 = QPushButton('Expand')
		btn2 = QPushButton('Collapse')
		btn0.clicked.connect(collapsible.toggle)
		btn1.clicked.connect(collapsible.expand)
		btn2.clicked.connect(collapsible.collapse)
		btnLayout.addWidget(btn1)
		btnLayout.addWidget(btn2)

		layout.addWidget(btn0)
		layout.addWidget(collapsible)
		layout.addLayout(btnLayout)
		layout.addStretch()

		return preview
	def createSlidingStackedPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('SlidingStacked'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		tmpLayout = QHBoxLayout()
		tmpLayout.setSpacing(20)
		tmpLayout.setAlignment(Qt.AlignLeft)

		ssw = SlidingStackedWidget()

		w1 = QPushButton('Page 1')
		w2 = QPushButton('Page 2')
		w3 = QPushButton('Page 3')
		w1.setStyleSheet("background-color: #7ce; border: 0; font-size: 24px; color: white;")
		w2.setStyleSheet("background-color: #bae; border: 0; font-size: 24px; color: white;")
		w3.setStyleSheet("background-color: gray; border: 0; font-size: 24px; color: white;")
		ssw.addWidget(w1)
		ssw.addWidget(w2)
		ssw.addWidget(w3)
		w2.setFixedHeight(100)
		# ssw.vertical = True
		ssw.wrap = True

		btn1 = QPushButton('Prev')
		btn1.clicked.connect(ssw.slideInPrev)

		btn2 = QPushButton('Next')
		btn2.clicked.connect(ssw.slideInNext)

		btnLayout = QHBoxLayout()
		btnLayout.addWidget(btn1)
		btnLayout.addWidget(btn2)

		tmpLayout.addWidget(ssw)
		
		layout.addLayout(btnLayout)
		layout.addLayout(tmpLayout)


		return preview
	def createSpinnerPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('WaitingSpinner'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		spinnerLayout = QHBoxLayout()
		spinnerLayout.setSpacing(50)
		spinnerLayout.setAlignment(Qt.AlignLeft)

		ws1 = WaitingSpinner()
		ws2 = WaitingSpinner(clockwise = False)
		ws3 = WaitingSpinner(color = QColor(50, 120, 200), clockwise = False)

		ws1.setFixedSize(50, 50)
		ws2.setFixedSize(50, 50)
		ws3.setFixedSize(50, 50)

		spinnerLayout.addWidget(ws1)
		spinnerLayout.addWidget(ws2)
		spinnerLayout.addWidget(ws3)
		
		layout.addLayout(spinnerLayout)


		return preview
	def createDataGridPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  RPOGRESSBAR  #############
		layout.addWidget(QLabel('DataGrid'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		datagridLayout = QHBoxLayout()
		datagridLayout.setSpacing(50)
		datagridLayout.setAlignment(Qt.AlignLeft)

		model = DataGrid()
		model.append('int var1', 'int')
		model.append('int var2', 'int')
		model.append('group var1', 'color', group = 'test_group', group_type = 'box_group' )
		model.append('int var3', 'int')
		model.append('float var1', 'float')
		model.append('float var2', 'float')
		model.append('string var1', 'string')
		model.append('string var2', 'string')
		model.append('group var2', 'color', group = 'test_group', group_type = 'box_group' )
		# model.append('var2', 'int', group = 'group1', group_type = 'title_group' )
		# model.append('var4', 'int', group = 'group2', group_type = 'title_group' )
		model.buildGroups()

		view = DataGridView()
		view.setDataGrid(model)

		datagridLayout.addWidget(view)
		
		layout.addLayout(datagridLayout)


		return preview

	def minimumSizeHint(self):
		return QSize(300, 100)

