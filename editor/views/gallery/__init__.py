from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.complex.tree_stacked import TreeStackedWidget
from editor.models.editor.property_model import PropertyModel, PropertyType, GroupType
from editor.widgets.complex.sliding_stacked import SlidingStackedWidget
from editor.widgets.drawers import DataGridDrawer
from editor.widgets.basic.button import MenuPopupToolButton, ButtonGroup
from editor.widgets.basic.slider import RangeSlider, Slider
from editor.widgets.basic.progress_bar import ProgressBar
from editor.widgets.basic.line_edit import LineEdit, IntLineEdit, FloatLineEdit, SearchLineEdit, PlaceholderLineEdit, PathLineEdit
from editor.widgets.basic.vector_edit import Vector2Edit, Vector3Edit, Vector4Edit, Vector4IntEdit, RectEdit
from editor.widgets.basic.drop_down import DropDown, FlagDropDown
from editor.widgets.basic.text_area import TextArea
from editor.widgets.basic.color_edit import ColorEdit
from editor.widgets.basic.object_edit import ObjectEdit
from editor.widgets.basic.spinner import WaitingSpinner, CircleSpinner
from editor.widgets.group.simple_group import SimpleGroup
from editor.widgets.group.box_group import BoxGroup
from editor.widgets.group.tab_group import TabGroup
from editor.widgets.group.foldout_group import FoldoutGroup
from editor.widgets.group.title_group import TitleGroup
from editor.widgets.misc.collapsible import CollapsibleWidget
from editor.widgets.misc.info_box import InfoBox
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
		treeStacked.addStackedWidget('Basic/Vector', self.createVectorPreview())
		treeStacked.addStackedWidget('Group', self.createGroupPreview())
		treeStacked.addStackedWidget('Complex/SlidingStacked', self.createSlidingStackedPreview())
		treeStacked.addStackedWidget('Complex/CurveEditor', None)
		treeStacked.addStackedWidget('Complex/ListDrawer', None)
		treeStacked.addStackedWidget('Complex/DictDrawer', None)
		treeStacked.addStackedWidget('Complex/DataGrid', self.createDataGridPreview())
		treeStacked.addStackedWidget('Misc/Collapsible', self.createCollapsiblePreview())
		treeStacked.addStackedWidget('Misc/InfoBox', self.createInfoBoxPreview())
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
		pushBtn2.setCheckable(True)
		pushBtn2.setChecked(True)
		pushBtn3 = QPushButton('popup')
		pushBtn3.setMenu(createTestMenu(pushBtn3))

		pushBtn4 = QPushButton(getThemeIcon('project.png'), 'all')
		pushBtn4.setMenu(createTestMenu(pushBtn4))

		pushBtn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		pushBtn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		pushBtn3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		pushBtn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		pushBtnLayout.addWidget(pushBtn1)
		pushBtnLayout.addWidget(pushBtn2)
		pushBtnLayout.addWidget(pushBtn3)
		pushBtnLayout.addWidget(pushBtn4)
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
		toolBtn2 = MenuPopupToolButton()
		toolBtn2.setIcon(getThemeIcon('project.png'))
		toolBtn3 = QToolButton()
		toolBtn3.setIcon(getThemeIcon('project.png'))
		toolBtn3.setPopupMode(QToolButton.InstantPopup)
		toolBtn3.setMenu(createTestMenu(toolBtn3))
		toolBtn4 = QToolButton()
		toolBtn4.setText('popup')
		toolBtn4.setPopupMode(QToolButton.InstantPopup)
		toolBtn4.setMenu(createTestMenu(toolBtn4))
		toolBtn5 = MenuPopupToolButton()
		toolBtn5.setText('popup')

		toolBtn1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		toolBtn2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		toolBtn3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		toolBtn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		toolBtn5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		toolBtnLayout.addWidget(toolBtn1)
		toolBtnLayout.addWidget(toolBtn2)
		toolBtnLayout.addWidget(toolBtn3)
		toolBtnLayout.addWidget(toolBtn4)
		toolBtnLayout.addWidget(toolBtn5)
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
		dropdown1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		dropdown1.setFocusPolicy(Qt.StrongFocus)

		dropdown2 = DropDown()
		dropdown2.setItems([f'Item {x}' for x in range(40)])
		dropdown2.setCurrentIndex(3)
		dropdown2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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
		flag1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		flag1.setFocusPolicy(Qt.StrongFocus)

		flag2 = FlagDropDown()
		flag2.setItems([f'Item {x}' for x in range(40)])
		flag2.setCurrentIndex(127)
		flag2.setFlag('Item 0', False)
		flag2.setCurrentIndex(0)
		QTimer.singleShot(111, lambda:flag2.setCurrentIndex(0))
		flag2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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
		checkBox2 = QCheckBox('tristate')
		checkBox2.setTristate(True)
		# checkBox2.setIcon(getThemeIcon('project.png'))
		checkBox2.setFocusPolicy(Qt.StrongFocus)

		radioBtn1 = QRadioButton('radio 1')
		radioBtn1.setFocusPolicy(Qt.StrongFocus)
		radioBtn2 = QRadioButton('radio 2')
		radioBtn2.setFocusPolicy(Qt.StrongFocus)

		checkBoxLayout.addWidget(checkBox1)
		checkBoxLayout.addWidget(checkBox2)

		checkBoxLayout.addSpacing(20)
		checkBoxLayout.addWidget(radioBtn1)
		checkBoxLayout.addWidget(radioBtn2)
		layout.addLayout(checkBoxLayout)


		#############  BUTTONGROUP  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ButtonGroup'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		btnGroupLayout = QHBoxLayout()
		btnGroupLayout.setSpacing(20)
		btnGroupLayout.setAlignment(Qt.AlignLeft)

		btnGroup = ButtonGroup()
		btnGroup.initFromItems([f'Item {i}' for i in range(4)])
		btnGroup.select(0)
		btnGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		btnGroupLayout.addWidget(btnGroup)
		layout.addLayout(btnGroupLayout)

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


		#############  OBJECT  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ObjectEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		referanceEditLayout = QHBoxLayout()
		referanceEditLayout.setSpacing(20)
		referanceEditLayout.setAlignment(Qt.AlignLeft)

		referanceEdit = ObjectEdit()

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


		#############  TEXTAREA  #############
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

		slider = Slider(Qt.Horizontal)
		slider.setMinimum(0)
		slider.setMaximum(100)
		slider.setSingleStep(1)
		slider.setFixedWidth(200)
		slider.setValue(20)
		slider.valueChanged.connect(lambda v: progressBar.setValue(v))
		slider.setFocusPolicy(Qt.StrongFocus)

		rangeSlider = RangeSlider()
		rangeSlider.setFixedWidth(200)
		rangeSlider.setFocusPolicy(Qt.StrongFocus)

		sliderLayout.addWidget(slider)
		sliderLayout.addWidget(rangeSlider)
		layout.addLayout(sliderLayout)

		return preview
	def createCollapsiblePreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  COLLAPSIBLE  #############
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


		#############  SLIDINGSTACKED  #############
		layout.addWidget(QLabel('SlidingStacked'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		tmpLayout = QHBoxLayout()
		tmpLayout.setSpacing(20)
		tmpLayout.setAlignment(Qt.AlignLeft)

		ssw = SlidingStackedWidget()
		ssw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		ssw.setObjectName('preview')

		w1 = QPushButton('Page 1')
		w2 = QPushButton('Page 2')
		w3 = QPushButton('Page 3')
		w1.setStyleSheet("background-color: #7ce; border: 0; font-size: 24px; color: white;")
		w2.setStyleSheet("background-color: #bae; border: 0; font-size: 24px; color: white;")
		w3.setStyleSheet("background-color: gray; border: 0; font-size: 24px; color: white;")
		ssw.addWidget(w1)
		ssw.addWidget(w2)
		ssw.addWidget(w3)
		w1.setFixedHeight(200)
		w2.setFixedHeight(400)
		w3.setFixedHeight(300)
		ssw.initWidget()

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
		layout.addWidget(QPushButton('Placeholder'))


		return preview
	def createSpinnerPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  WAITINGSPINNER  #############
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


		#############  CIRCLESPINNER  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('CircleSpinner'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		spinnerLayout = QHBoxLayout()
		spinnerLayout.setSpacing(50)
		spinnerLayout.setAlignment(Qt.AlignLeft)

		ws1 = CircleSpinner()
		ws2 = CircleSpinner(clockwise = False)
		ws3 = CircleSpinner(arcColor = QColor(50, 200, 120), clockwise = False)

		ws1.setFixedSize(50, 50)
		ws2.setFixedSize(50, 50)
		ws3.setFixedSize(50, 50)

		spinnerLayout.addWidget(ws1)
		spinnerLayout.addWidget(ws2)
		spinnerLayout.addWidget(ws3)
		
		layout.addLayout(spinnerLayout)


		return preview
	def createVectorPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  VECTOR  #############
		layout.addWidget(QLabel('VectorEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		vec2 = Vector2Edit()
		vec3 = Vector3Edit()
		vec4 = Vector4Edit()
		vec4Int = Vector4IntEdit()
		rect = RectEdit()

		layout.addWidget(vec2)
		layout.addWidget(vec3)
		layout.addWidget(vec4)
		layout.addWidget(vec4Int)

		layout.addSpacing(20)
		layout.addWidget(QLabel('RectEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		layout.addWidget(rect)
		
		return preview
	def createInfoBoxPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  INFOBOX  #############
		layout.addWidget(QLabel('InfoBox'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		infoBox = InfoBox('This is a info box.')
		warnBox = InfoBox('This is a warning box.\nAnd support multiline message.', 'warn')
		errorBox = InfoBox('This is a error box.\nSingle line text which too long will be wrapped by word automatically.', 'error')
		layout.addWidget(infoBox)
		layout.addWidget(warnBox)
		layout.addWidget(errorBox)
		
		return preview
	def createGroupPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(20)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)

		titleGroup = TitleGroup('TitleGroupName')
		titleGroup.layout().addWidget(QPushButton('Hello'))
		titleGroup.layout().addWidget(QPushButton('World'))
		titleGroup.layout().setSpacing(2)
		titleGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		layout.addWidget(titleGroup)

		simpleGroup = SimpleGroup('SimpleGroupName')
		simpleGroup.container.layout().addWidget(QPushButton('Hello'))
		simpleGroup.container.layout().addWidget(QPushButton('World'))
		simpleGroup.container.layout().setSpacing(2)
		simpleGroup.updateFixedHeight()
		simpleGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		layout.addWidget(simpleGroup)

		boxGroup = BoxGroup('BoxGroupName')
		boxGroup.layout().addWidget(QPushButton('Hello'))
		boxGroup.layout().addWidget(QPushButton('World'))
		boxGroup.layout().setSpacing(2)
		boxGroup.horizontalPadding = 3
		boxGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		layout.addWidget(boxGroup)

		foldoutGroup = FoldoutGroup('FoldoutGroupName')
		foldoutGroup.container.layout().addWidget(QPushButton('Hello'))
		foldoutGroup.container.layout().addWidget(QPushButton('World'))
		foldoutGroup.container.layout().setSpacing(2)
		foldoutGroup.updateFixedHeight()
		foldoutGroup.horizontalPadding = 3
		foldoutGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		layout.addWidget(foldoutGroup)

		tabGroup = TabGroup()

		tabContent1 = QWidget()
		contentLayout1 = QVBoxLayout()
		contentLayout1.setContentsMargins(3, 3, 3, 3)
		contentLayout1.setSpacing(2)
		contentLayout1.addWidget(QPushButton('Hello'))
		contentLayout1.addWidget(QPushButton('World'))
		tabContent1.setLayout(contentLayout1)

		tabContent2 = QWidget()
		contentLayout2 = QVBoxLayout()
		contentLayout2.setContentsMargins(3, 3, 3, 3)
		contentLayout2.setSpacing(2)
		contentLayout2.addWidget(QPushButton('Hello'))
		contentLayout2.addWidget(QPushButton('World'))
		contentLayout2.addWidget(QPushButton('Emmmm'))
		tabContent2.setLayout(contentLayout2)

		tabContent3 = QWidget()
		contentLayout3 = QVBoxLayout()
		contentLayout3.setContentsMargins(3, 3, 3, 3)
		contentLayout3.setSpacing(2)
		contentLayout3.addWidget(QPushButton('Hello'))
		contentLayout3.addWidget(QPushButton('World3'))
		tabContent3.setLayout(contentLayout3)

		tabContent4 = QWidget()
		contentLayout4 = QVBoxLayout()
		contentLayout4.setContentsMargins(3, 3, 3, 3)
		contentLayout4.setSpacing(2)
		contentLayout4.addWidget(QPushButton('Hello'))
		contentLayout4.addWidget(QPushButton('World'))
		tabContent4.setLayout(contentLayout4)

		tabContent1.setFixedHeight(tabContent1.sizeHint().height())
		tabContent2.setFixedHeight(tabContent2.sizeHint().height())
		tabContent3.setFixedHeight(tabContent3.sizeHint().height())
		tabContent4.setFixedHeight(tabContent4.sizeHint().height())

		tabGroup.container.addWidget(tabContent1)
		tabGroup.container.addWidget(tabContent2)
		tabGroup.container.addWidget(tabContent3)
		tabGroup.container.addWidget(tabContent4)
		tabGroup.container.initWidget()
		layout.addWidget(tabGroup)

		return preview
	def createDataGridPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  DATAGRID  #############
		layout.addWidget(QLabel('DataGrid'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)

		datagridLayout = QHBoxLayout()
		datagridLayout.setSpacing(50)
		datagridLayout.setAlignment(Qt.AlignLeft)

		model = PropertyModel()
		model.append('int var1', PropertyType.Int)
		model.append('int var2', PropertyType.Int)
		model.append('group var1', PropertyType.Object, group = 'test_group1', group_type = GroupType.BoxGroup)
		model.append('title var1', PropertyType.Color, group = 'test_group2', group_type = GroupType.TitleGroup)
		model.append('int var3', PropertyType.Int)
		# model.append('path var1', PropertyType.Path)
		# model.append('path var2', PropertyType.Path)
		model.append('float var1', PropertyType.Float)
		model.append('float var2', PropertyType.Float)
		model.append('string var1', PropertyType.String)
		model.append('string var2', PropertyType.String)
		model.append('group var2', PropertyType.Object, group = 'test_group1', group_type = GroupType.BoxGroup)
		model.append('title var2', PropertyType.Color, group = 'test_group2', group_type = GroupType.TitleGroup)
		model.commit()

		drawer = DataGridDrawer()
		drawer.setPropertyModel(model)

		datagridLayout.addWidget(drawer)
		
		layout.addLayout(datagridLayout)


		return preview

	def minimumSizeHint(self):
		return QSize(300, 100)

