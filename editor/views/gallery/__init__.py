from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from editor.widgets.complex.tree_view import TreeView
from editor.widgets.control.slider import Slider
from editor.widgets.misc.line import HLineWidget
from editor.common.icon_cache import getThemeIcon, getThemePixmap
from editor.common.util import createTestMenu
from editor.view_manager import DockView, dockView


@dockView('Gallery')
class GalleryView(DockView):
	def __init__(self, parent, **data):
		super().__init__(parent, **data)

		# layout = QHBoxLayout()
		# layout.setAlignment(Qt.AlignTop)
		# self.layout().addLayout(layout)

		tree = self.createTreeView()
		preview = self.createTestPreview()
		preview.setMinimumWidth(150)

		splitter = QSplitter(self)
		splitter.addWidget(tree)
		splitter.addWidget(preview)
		splitter.setOrientation(Qt.Horizontal)
		splitter.setChildrenCollapsible(False)
		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 3)

		self.setWidget(splitter)
		# self.layout().addWidget(splitter)

		tree.installEventFilter(self)
		self.tree = tree


	def createTreeView(self):
		view = TreeView(self)
		# view.setWindowFlags(Qt.Window)
		model = QStandardItemModel()
		for i in range(5):
			n = QStandardItem(f'Item_{i}')
			model.appendRow(n)
			for j in range(4):
				c = QStandardItem(f'Child_{j}')
				n.appendRow(c)

		# model.dataChanged.connect(lambda i1, i2, r: print(r))
		view.setModel(model)
		return view

	def createTestPreview(self):
		area = QScrollArea(self)
		area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		area.setWidgetResizable(True)

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
		# toolBtnLayout.setSpacing(5)
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


		#############  CHECKBOX  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('CheckBox and RadioButton'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		checkBoxLayout = QHBoxLayout()
		checkBoxLayout.setSpacing(20)
		checkBoxLayout.setAlignment(Qt.AlignLeft)

		checkBox1 = QCheckBox('normal')
		checkBox2 = QCheckBox('icon')
		checkBox2.setIcon(getThemeIcon('project.png'))

		radioBtn1 = QRadioButton('normal')
		radioBtn2 = QRadioButton('icon')
		radioBtn2.setIcon(getThemeIcon('project.png'))

		checkBoxLayout.addWidget(checkBox1)
		checkBoxLayout.addWidget(checkBox2)

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


		#############  LINEEDIT  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('LineEdit'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		comboBoxLayout = QHBoxLayout()
		comboBoxLayout.setSpacing(20)
		comboBoxLayout.setAlignment(Qt.AlignLeft)

		lineEdit1 = QLineEdit()
		lineEdit2 = QLineEdit()
		lineEdit2.setPlaceholderText('placeholder')

		comboBoxLayout.addWidget(lineEdit1)
		comboBoxLayout.addWidget(lineEdit2)
		layout.addLayout(comboBoxLayout)


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


		#############  RPOGRESSBAR  #############
		layout.addSpacing(20)
		layout.addWidget(QLabel('ProgressBar'))
		layout.addWidget(HLineWidget())
		layout.addSpacing(5)
		comboBoxLayout = QHBoxLayout()
		comboBoxLayout.setSpacing(20)
		comboBoxLayout.setAlignment(Qt.AlignLeft)

		progressBar = QProgressBar()
		progressBar.setValue(30)

		comboBoxLayout.addWidget(progressBar)
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
		slider1.setMinimum(10)
		slider1.setMaximum(50)
		slider1.setSingleStep(3) 
		slider1.setFixedWidth(100)
		slider1.setValue(20)
		slider2 = Slider()
		slider2.setFixedWidth(100)

		sliderLayout.addWidget(slider1)
		sliderLayout.addWidget(slider2)
		layout.addLayout(sliderLayout)

		area.setWidget(preview)
		return area
		# return preview

	def eventFilter(self, obj, evt):
		if evt.type() == QEvent.KeyPress:
			key = evt.key()
			if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_Up or key == Qt.Key_Down:
				self.tree.keyPressEvent(evt)
			return True
		return False

	def minimumSizeHint(self):
		return QSize(300, 100)

