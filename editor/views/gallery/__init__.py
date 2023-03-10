from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.complex.tree_stacked import TreeStackedWidget
from editor.widgets.basic.slider import RangeSlider
from editor.widgets.basic.line_edit import LineEdit
from editor.widgets.basic.search_edit import SearchEdit
from editor.widgets.container.collapsible import CollapsibleWidget
from editor.widgets.container.sliding_stacked import SlidingStackedWidget
from editor.widgets.misc.waiting_spinner import WaitingSpinner
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
		searchbar.setFixedHeight(25)
		searchbar.setObjectName('searchbar')
		searchbarLayout = QHBoxLayout(searchbar)
		searchbarLayout.setContentsMargins(0, 2, 2, 4)
		searchbarLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout.addWidget(searchbar)

		searchEdit = SearchEdit(self)
		searchEdit.setFixedWidth(300)
		searchbarLayout.addWidget(searchEdit)

		treeStacked = TreeStackedWidget(self)
		treeStacked.addStackedWidget('Basic/Button', self.createButtonPreview())
		treeStacked.addStackedWidget('Basic/CheckBox', self.createCheckBoxPreview())
		treeStacked.addStackedWidget('Basic/LineEdit', self.createLineEditPreview())
		treeStacked.addStackedWidget('Basic/Slider', self.createSliderPreview())
		treeStacked.addStackedWidget('Container/Collapsible', self.createCollapsiblePreview())
		treeStacked.addStackedWidget('Container/SlidingStacked', self.createSlidingStackedPreview())
		treeStacked.addStackedWidget('Misc/WaitingSpinner', self.createWaitingSpinnerPreview())
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


		return preview
	def createCheckBoxPreview(self):
		preview = QWidget(self)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setSpacing(5)
		# layout.setContentsMargins(0, 0, 0, 0)
		preview.setLayout(layout)


		#############  CHECKBOX  #############
		layout.addWidget(QLabel('CheckBox and RadioButton'))
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


		#############  COMBOXBOX  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ComboBox and SpinBox'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		comboBoxLayout = QHBoxLayout()
		comboBoxLayout.setSpacing(20)
		comboBoxLayout.setAlignment(Qt.AlignLeft)

		comboBox1 = QComboBox()
		comboBox1.addItems(['Zero', 'One', 'Two', 'Three'])
		comboBox1.setCurrentIndex(2)

		spinBox1 = QSpinBox()
		spinBox2 = QDoubleSpinBox()

		comboBox1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		spinBox1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		spinBox2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		comboBoxLayout.addWidget(comboBox1)
		comboBoxLayout.addWidget(spinBox1)
		comboBoxLayout.addWidget(spinBox2)
		layout.addLayout(comboBoxLayout)

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
		comboBoxLayout = QHBoxLayout()
		comboBoxLayout.setSpacing(20)
		comboBoxLayout.setAlignment(Qt.AlignLeft)

		lineEdit1 = QLineEdit()
		lineEdit2 = LineEdit()
		lineEdit2.setPlaceholderText('placeholder')

		comboBoxLayout.addWidget(lineEdit1)
		comboBoxLayout.addWidget(lineEdit2)
		layout.addLayout(comboBoxLayout)


		#############  SEARCH  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('SearchEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		searchEditLayout = QHBoxLayout()
		searchEditLayout.setSpacing(20)
		searchEditLayout.setAlignment(Qt.AlignLeft)

		searchEdit = SearchEdit()

		searchEditLayout.addWidget(searchEdit)
		layout.addLayout(searchEditLayout)


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

		progressBar = QProgressBar()
		progressBar.setValue(30)
		progressBar.setObjectName('test')
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
		slider1.setFixedWidth(100)
		slider1.setValue(20)
		slider1.sliderMoved.connect(lambda v: progressBar.setValue(v))
		slider1.setFocusPolicy(Qt.StrongFocus)
		slider2 = RangeSlider(Qt.Horizontal)
		slider2.setMinimumHeight(30)
		slider2.setMinimum(0)
		slider2.setMaximum(255)
		slider2.setLow(15)
		slider2.setHigh(35)
		slider2.setTickPosition(QSlider.TicksBelow)
		slider2.setFixedWidth(100)

		sliderLayout.addWidget(slider1)
		sliderLayout.addWidget(slider2)
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
		tmpLayout = QHBoxLayout()
		tmpLayout.setSpacing(20)
		tmpLayout.setAlignment(Qt.AlignLeft)

		wgt = CollapsibleWidget()

		tmpLayout.addWidget(wgt)
		layout.addLayout(tmpLayout)


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
		w1.setStyleSheet("background-color: blue ; border: 0; font-size: 24px; color: white;")
		w2.setStyleSheet("background-color: green; border: 0; font-size: 24px; color: white;")
		w3.setStyleSheet("background-color: gray ; border: 0; font-size: 24px; color: white;")
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
	def createWaitingSpinnerPreview(self):
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

	def minimumSizeHint(self):
		return QSize(300, 100)

