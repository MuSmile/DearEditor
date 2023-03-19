import time, functools
from enum import Enum
from math import floor
from PySide6.QtCore import Qt, Property, QSize, QRect, QTimer, QPointF, QItemSelectionModel, QEvent
from PySide6.QtWidgets import QTreeView, QWidget, QApplication, QItemDelegate, QStyle, QStyleOption
from PySide6.QtGui import QPen, QPainter, QColor, QDrag, QCursor, QPixmap, QMouseEvent
from editor.common.math import clamp, lerp
from editor.common.ease import easeInOutQuad, easeOutQuad
from editor.common.util import modelIndexDepth, isChildOfModelIndex, isAboveOfModelIndex
from editor.common.icon_cache import getThemePixmap


class TreeItemDelegate(QItemDelegate):
	def __init__(self, view):
		super().__init__()
		self.view = view

	def sizeHint(self, option, index):
		w = option.rect.width()
		h = index.data(Qt.SizeHintRole)
		if h == None: h = self.view.itemHeight
		return QSize(w, h)

	def updateEditorGeometry(self, editor, option, index):
		view = self.view
		rect = view.visualRect(index)
		left = rect.x() + view.treePaddingLeft
		if index.data(Qt.DecorationRole): left += view.indentation() + view.itemPaddingLeft
		rect.setLeft(left - 3)
		if view.useBackgroundSeparator: rect.setHeight(rect.height() - 1)
		editor.setGeometry(rect)

	def paint(self, painter, option, index):
		painter.setRenderHint(QPainter.Antialiasing, True)
		painter.setRenderHint(QPainter.TextAntialiasing, True)
		# painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

		view = self.view
		rect = option.rect
		rect.setHeight(view.itemHeight)

		l, r = rect.left(), rect.right() + 1
		t, h = rect.top(), rect.height()

		ch = index.data(Qt.SizeHintRole)
		if ch == None: ch = self.view.itemHeight
		painter.setClipRect(QRect(0, t, r, ch))

		bgRect = QRect(0, t, r, h)
		branchRect = QRect(0, t, l, h)
		self.drawBackground(painter, bgRect, option.state, index)
		self.drawBranchLines(painter, branchRect, index)
		self.drawBranchArrow(painter, branchRect, index)
		self.drawContent(painter, rect, index)

	def drawBackground(self, painter, rect, state, index):
		view = self.view
		selected = state & QStyle.State_Selected
		hovered  = index == view.hoveredIndex # option.state & QStyle.State_MouseOver
		bgColor  = None
		if selected:
			bgColor = view.backgroundSelected if view.viewFocused else view.backgroundSelectedUnfocused
		elif hovered and view.dropIndicatorRect == None:
			bgColor = view.backgroundHovered
		else:
			# alternate = option.features & QStyleOptionViewItem.Alternate
			alternate = view.useAlternatingBackground and self.view._flatVisibleRowNumber(index, self.view.model()) % 2
			bgColor = view.backgroundAlternate if alternate else view.background
		painter.fillRect(rect, bgColor)
		b, w = rect.bottom(), rect.width()

		if view.useBackgroundSeparator:
			srect = QRect(0, b, w, 1)
			painter.fillRect(srect, view.backgroundSeparator)

	def drawContent(self, painter, rect, index):
		view = self.view
		textOffset = view.treePaddingLeft
		decoration = index.data(Qt.DecorationRole)

		if decoration:
			indentation = view.indentation()
			rectSize = view.itemHeight
			textOffset += indentation + view.itemPaddingLeft
			cx, cy = rect.left() + round(indentation / 2), rect.top() + round(rect.height() / 2) - 1
			iconSize = view.itemIconSize
			halfSize = iconSize / 2
			x, y = cx - halfSize + view.treePaddingLeft, cy - halfSize
			painter.drawPixmap(x, y, iconSize, iconSize, decoration)

		painter.drawText(rect.adjusted(textOffset, -1, 0, 0), Qt.AlignVCenter, index.data())
	
	def drawBranchLines(self, painter, rect, index):
		view = self.view
		if not view.drawBranchLine: return

		itemDepth = modelIndexDepth(index)
		drawDepth = itemDepth - view.branchLineFilterDepth
		if drawDepth >= 0:
			painter.setOpacity(0.4)
			indentation = view.indentation()
			t, h = rect.top(), rect.height()
			# print(index.siblingAtRow(index.row()+1).isValid(), index.data())
			curr = index
			for i in range(drawDepth):
				x = int(indentation * (itemDepth - i - 0.5)) + view.treePaddingLeft
				# painter.fillRect(x, t, indentation, h, Qt.green)
				hasSiblings = curr.siblingAtRow(curr.row() + 1).isValid()
				adjoinsItem = i == 0
				if hasSiblings:
					if not adjoinsItem:
						painter.drawPixmap(x, t, indentation, h, getThemePixmap('icon_branch_I.png'))
					else:
						painter.drawPixmap(x, t, indentation, h, getThemePixmap('icon_branch_T.png'))
				elif not hasSiblings and adjoinsItem:
					painter.drawPixmap(x, t, indentation, h, getThemePixmap('icon_branch_L.png'))
				curr = curr.parent()
			painter.setOpacity(1)
	
	def drawBranchArrow(self, painter, rect, index):
		if not index.model().hasChildren(index): return

		view = self.view
		size = view.branchPixmapSize
		sizeHalf = size / 2
		cx = rect.right() - round(view.indentation() / 2) + 1 + view.treePaddingLeft
		cy = rect.top() + (rect.height() / 2)
		rect = QRect(cx - sizeHalf - view.branchArrowOffset, cy - sizeHalf, size, size)
		branchArrow = view.isExpanded(index) and view.branchOpened or view.branchClosed
		painter.drawPixmap(rect, branchArrow)

class PingAnimPhase(Enum):
	ZoomIn  = 0
	ZoomOut = 2
	Idle    = 3
	Fade    = 4

class TreeItemPingOverlay(QWidget):
	InstanceTable = {}

	@Property(int)
	def pingZoomDuration(self):
		return self._pingZoomDuration
	@pingZoomDuration.setter
	def pingZoomDuration(self, value):
		self._pingZoomDuration = value

	@Property(int)
	def pingIdleDuration(self):
		return self._pingIdleDuration
	@pingIdleDuration.setter
	def pingIdleDuration(self, value):
		self._pingIdleDuration = value

	@Property(int)
	def pingFadeDuration(self):
		return self._pingFadeDuration
	@pingFadeDuration.setter
	def pingFadeDuration(self, value):
		self._pingFadeDuration = value

	@Property(float)
	def pingZoomScale(self):
		return self._pingZoomScale
	@pingZoomScale.setter
	def pingZoomScale(self, value):
		self._pingZoomScale = value

	@Property(int)
	def pingAnimTickInterval(self):
		return self._pingAnimTickInterval
	@pingAnimTickInterval.setter
	def pingAnimTickInterval(self, value):
		self._pingAnimTickInterval = value

	@Property(QColor)
	def pingOutlineColor(self):
		return self._pingOutlinePen.color()
	@pingOutlineColor.setter
	def pingOutlineColor(self, value):
		self._pingOutlinePen.setColor(value)
	@Property(int)
	def pingOutlineWidth(self):
		return self._pingOutlinePen.width()
	@pingOutlineWidth.setter
	def pingOutlineWidth(self, value):
		self._pingOutlinePen.setWidth(value)

	@Property(int)
	def pingOutlineRound(self):
		return self._pingOutlineRound
	@pingOutlineRound.setter
	def pingOutlineRound(self, value):
		self._pingOutlineRound = value

	def __init__(self, view):
		super().__init__(view)
		self._pingZoomDuration = 100
		self._pingIdleDuration = 2000
		self._pingFadeDuration = 1000
		self._pingZoomScale = 1.5
		self._pingAnimTickInterval = 16
		self._pingOutlinePen = QPen(QColor('#D7C11B'), 2)
		self._pingOutlineRound = 6

		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_DeleteOnClose, True)

		view.installEventFilter(self)

	def syncTreeViewRect(self):
		view = self.parent()
		viewport = view.viewport()
		self.setGeometry(viewport.rect())

	def eventFilter(self, obj, evt):
		if evt.type() == QEvent.Resize: self.syncTreeViewRect()
		return False

	def startPing(self, index):
		self.elapsed = 0
		self.progress = 0
		self.index = index
		self.state = PingAnimPhase.Idle

		view = self.parent()
		table = TreeItemPingOverlay.InstanceTable
		if view not in table: table[ view ] = []
		list = table[ view ]
		instanceCount = len(list)
		for i in range(instanceCount):
			instance = list[instanceCount - i - 1]
			if (instance.index == index): instance.stopPing()
		list.append(self)

		self.timer = QTimer()
		self.timer.timeout.connect(self.tickPingAnim)
		self.timer.start(self._pingAnimTickInterval)
		self.prevTickTime = time.time()
		self.syncTreeViewRect()

	def stopPing(self):
		view = self.parent()
		table = TreeItemPingOverlay.InstanceTable
		table[ view ].remove(self)
		self.timer.stop()
		self.timer.deleteLater()
		self.deleteLater()

	@staticmethod
	def stopAll(view):
		table = TreeItemPingOverlay.InstanceTable
		if view not in table: return
		list = table[ view ]
		instanceCount = len(list)
		for i in range(instanceCount):
			instance = list[instanceCount - i - 1]
			instance.stopPing()

	def tickPingAnim(self):
		curr = time.time()
		delta = (curr - self.prevTickTime) * 1000
		self.prevTickTime = curr
		self.elapsed += delta
		
		zoomInDuration = self._pingZoomDuration
		zoomOutDuration = zoomInDuration + self._pingZoomDuration
		idleDuration = zoomInDuration + self._pingIdleDuration
		fadeDuration = idleDuration + self._pingFadeDuration

		if self.elapsed <= zoomInDuration:
			self.state = PingAnimPhase.ZoomIn
			self.progress = self.elapsed / self._pingZoomDuration
			self.repaint()

		elif self.elapsed <= zoomOutDuration:
			self.state = PingAnimPhase.ZoomOut
			self.progress = (self.elapsed - zoomInDuration) / self._pingZoomDuration
			self.repaint()

		elif self.elapsed <= idleDuration:
			self.state = PingAnimPhase.Idle
			self.repaint()

		elif self.elapsed <= fadeDuration:
			self.state = PingAnimPhase.Fade
			k = (self.elapsed - idleDuration) / self._pingFadeDuration
			self.progress = easeOutQuad(k)
			self.repaint()

		else:
			return self.stopPing()

	def paintEvent(self, event):
		view = self.parent()
		index = self.index

		rect = view.visualRect(index)
		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing, True)
		painter.setRenderHints(QPainter.TextAntialiasing, True)

		option = QStyleOption()
		option.initFrom(self)
		fm = option.fontMetrics
		tp, ip = view.treePaddingLeft, view.itemPaddingLeft
		width = option.fontMetrics.boundingRect(index.data()).width() + tp * 2
		if index.data(Qt.DecorationRole): width += view.indentation() + ip + round((view.itemHeight - view.itemIconSize) / 2)
		rect.setWidth(width)

		zoom = None
		if self.state == PingAnimPhase.ZoomIn:
			zoom = lerp(1, self.pingZoomScale, self.progress)
		elif self.state == PingAnimPhase.ZoomOut:
			zoom = lerp(self.pingZoomScale, 1, self.progress)
		elif self.state == PingAnimPhase.Fade:
			painter.setOpacity(1 - self.progress)

		if zoom != None:
			tx, ty = rect.x() + width / 2, rect.y() + rect.height() / 2
			painter.translate(tx, ty)
			painter.scale(zoom, zoom)
			painter.translate(-tx, -ty)

		pen = painter.pen()
		alternate = view._flatVisibleRowNumber(index, view.model()) % 2
		bgColor = alternate and view.background or view.backgroundAlternate
		painter.setBrush(bgColor)
		painter.setPen(self._pingOutlinePen)
		painter.drawRoundedRect(rect.adjusted(-12 + tp, 0, 12 - tp, 0), self._pingOutlineRound, self._pingOutlineRound)

		painter.setPen(pen)
		delegate = view.itemDelegate(index)
		delegate.drawContent(painter, rect, index)

class TreeView(QTreeView):
	@Property(int)
	def treePaddingLeft(self):
		return self._treePaddingLeft
	@treePaddingLeft.setter
	def treePaddingLeft(self, value):
		if self._treePaddingLeft == value: return
		self._treePaddingLeft = value
		self.repaint()

	@Property(int)
	def itemPaddingLeft(self):
		return self._itemPaddingLeft
	@itemPaddingLeft.setter
	def itemPaddingLeft(self, value):
		if self._itemPaddingLeft == value: return
		self._itemPaddingLeft = value
		self.repaint()

	@Property(int)
	def itemIconSize(self):
		return self._itemIconSize
	@itemIconSize.setter
	def itemIconSize(self, value):
		if self._itemIconSize == value: return
		self._itemIconSize = value
		self.repaint()

	@Property(int)
	def itemHeight(self):
		return self._itemHeight
	@itemHeight.setter
	def itemHeight(self, value):
		if self._itemHeight == value: return
		self._itemHeight = value
		self.repaint()

	@Property(int)
	def branchPixmapSize(self):
		return self._branchPixmapSize
	@branchPixmapSize.setter
	def branchPixmapSize(self, value):
		if self._branchPixmapSize == value: return
		self._branchPixmapSize = value
		self.repaint()

	@Property(QPixmap)
	def branchOpened(self):
		return self._pixmapBranchOpened
	@branchOpened.setter
	def branchOpened(self, value):
		if self._pixmapBranchOpened == value: return
		self._pixmapBranchOpened = value
		self.repaint()

	@Property(QPixmap)
	def branchClosed(self):
		return self._pixmapBranchClosed
	@branchClosed.setter
	def branchClosed(self, value):
		if self._pixmapBranchClosed == value: return
		self._pixmapBranchClosed = value
		self.repaint()

	@Property(int)
	def branchArrowOffset(self):
		return self._branchArrowOffset
	@branchArrowOffset.setter
	def branchArrowOffset(self, value):
		self._branchArrowOffset = value

	@Property(bool)
	def customAnimated(self):
		return self._customAnimated
	@customAnimated.setter
	def customAnimated(self, value):
		self._customAnimated = value

	@Property(int)
	def customAnimDuration(self):
		return self._customAnimDuration
	@customAnimDuration.setter
	def customAnimDuration(self, value):
		self._customAnimDuration = value

	@Property(int)
	def customAnimTickInterval(self):
		return self._customAnimTickInterval
	@customAnimTickInterval.setter
	def customAnimTickInterval(self, value):
		self._customAnimTickInterval = value

	@Property(int)
	def dropIndicatorMargin(self):
		return self._dropIndicatorMargin
	@dropIndicatorMargin.setter
	def dropIndicatorMargin(self, value):
		self._dropIndicatorMargin = value

	@Property(QColor)
	def dropIndicatorColor(self):
		return self._penDropIndicator.color()
	@dropIndicatorColor.setter
	def dropIndicatorColor(self, value):
		if self._penDropIndicator.color() == value: return
		self._penDropIndicator.setColor(value)
		self.repaint()
	@Property(int)
	def dropIndicatorWidth(self):
		return self._penDropIndicator.width()
	@dropIndicatorWidth.setter
	def dropIndicatorWidth(self, value):
		if self._penDropIndicator.width() == value: return
		self._penDropIndicator.setWidth(value)
		self.repaint()

	@Property(bool)
	def drawBranchLine(self):
		return self._drawBranchLine
	@drawBranchLine.setter
	def drawBranchLine(self, value):
		self._drawBranchLine = value
	@Property(int)
	def branchLineFilterDepth(self):
		return self._branchLineFilterDepth
	@branchLineFilterDepth.setter
	def branchLineFilterDepth(self, value):
		self._branchLineFilterDepth = value

	@Property(QColor)
	def background(self):
		return self._background
	@background.setter
	def background(self, value):
		self._background = value
	@Property(QColor)
	def backgroundAlternate(self):
		return self._backgroundAlternate
	@backgroundAlternate.setter
	def backgroundAlternate(self, value):
		self._backgroundAlternate = value
	@Property(QColor)
	def backgroundSelected(self):
		return self._backgroundSelected
	@backgroundSelected.setter
	def backgroundSelected(self, value):
		self._backgroundSelected = value
	@Property(QColor)
	def backgroundSelectedUnfocused(self):
		return self._backgroundSelectedUnfocused
	@backgroundSelectedUnfocused.setter
	def backgroundSelectedUnfocused(self, value):
		self._backgroundSelectedUnfocused = value
	@Property(QColor)
	def backgroundHovered(self):
		return self._backgroundHovered
	@backgroundHovered.setter
	def backgroundHovered(self, value):
		self._backgroundHovered = value
	@Property(bool)
	def useAlternatingBackground(self):
		return self._useAlternatingBackground
	@useAlternatingBackground.setter
	def useAlternatingBackground(self, value):
		self._useAlternatingBackground = value

	@Property(QColor)
	def backgroundSeparator(self):
		return self._backgroundSeparator
	@backgroundSeparator.setter
	def backgroundSeparator(self, value):
		self._backgroundSeparator = value
	@Property(bool)
	def useBackgroundSeparator(self):
		return self._useBackgroundSeparator
	@useBackgroundSeparator.setter
	def useBackgroundSeparator(self, value):
		self._useBackgroundSeparator = value

	
	def __init__(self, parent = None):
		super().__init__(parent)
		self._treePaddingLeft = 2
		self._itemPaddingLeft = 2
		self._itemIconSize = 16
		self._penDropIndicator = QPen(QColor('#8af'), 2)
		self._branchPixmapSize = 12
		self._pixmapBranchOpened = getThemePixmap('arrow_down.png')
		self._pixmapBranchClosed = getThemePixmap('arrow_right.png')
		self._branchArrowOffset = 0
		self._customAnimated = True
		self._customAnimDuration = 120
		self._customAnimTickInterval = 16
		self._dropIndicatorMargin = 5
		self._itemHeight = 20
		self._drawBranchLine = True
		self._branchLineFilterDepth = 1
		self.setIndentation(20)

		self._background = QColor('#404040')
		self._backgroundAlternate = QColor('#474747')
		self._backgroundSelected = QColor('#515c84')
		self._backgroundSelectedUnfocused = QColor('#6d7284')
		self._backgroundHovered = QColor('#454768')
		self._useAlternatingBackground = True
		self._backgroundSeparator = QColor('#2c2c2c')
		self._useBackgroundSeparator = True

		self.hoveredIndex = None
		self.underAnimating = None
		self.collapsingIndex = None
		self.dropIndicatorRect = None
		self.dropPosition = None # -1 - before, 0 - inside, 1 - after

		self.viewFocused = None

		self.autoExpandTimer = QTimer()
		self.autoExpandTimer.timeout.connect(self.expandHovered)
		self.autoExpandTimer.setSingleShot(True)
		
		self.setMouseTracking(True)
		self.setItemDelegate(TreeItemDelegate(self))

		self.setAnimated(False)
		self.setHeaderHidden(True)
		self.setAlternatingRowColors(False)
		self.setExpandsOnDoubleClick(False)
		self.setItemsExpandable(False)
		self.setFocusPolicy(Qt.ClickFocus)

		self.dropAccepted = None
		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setDragDropMode(self.InternalMove)
		self.setSelectionMode(self.ExtendedSelection)

		self.setEditTriggers(self.SelectedClicked)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setVerticalScrollMode(self.ScrollPerPixel)
		# self.verticalScrollBar().setSingleStep(5)

		self.verticalScrollBar().valueChanged.connect(self.onScrollerValueChange)


	#################  EVENTS  #################
	def updateViewFocused(self, focused):
		if self.viewFocused == focused: return
		self.viewFocused = focused
		self.repaint()
	def focusInEvent(self, evt):
		self.updateViewFocused(True)
	def focusOutEvent(self, evt):
		# to do: handle context menu
		self.updateViewFocused(False)

	def testClickBranchArrow(self, evt, doubleClick):
		# if self.underAnimating: return True
		pos = evt.pos()
		index = self.indexAt(pos)
		if not self.model().hasChildren(index): return False
		rect = self.visualRect(index)
		l, t, h = rect.left(), rect.top(), rect.height()
		indentation = self.indentation()
		branchRect = QRect(l - indentation + self.treePaddingLeft - self.branchArrowOffset, t, indentation, h)
		if branchRect.contains(pos):
			recursive = evt.modifiers() == Qt.AltModifier
			self.toggleExpand(index, recursive)
			return True

		if pos.x() < l + self.treePaddingLeft:
			newPos = QPointF(l, pos.y())
			newPosGlobal = self.mapToGlobal(newPos)
			newEvt = QMouseEvent(evt.type(), newPos, newPosGlobal, evt.button(), evt.buttons(), evt.modifiers())
			if doubleClick:
				super().mouseDoubleClickEvent(newEvt)
			else:
				super().mousePressEvent(newEvt)
			return True

	def mousePressEvent(self, evt):
		TreeItemPingOverlay.stopAll(self)
		if self.testClickBranchArrow(evt, False): return
		super().mousePressEvent(evt)

	def mouseReleaseEvent(self, evt):
		pos = evt.pos()
		index = self.indexAt(pos)
		rect = self.visualRect(index)
		l, t, h = rect.left(), rect.top(), rect.height()
		indentation = self.indentation()
		branchRect = QRect(l - indentation + self.treePaddingLeft, t, indentation, h)
		if branchRect.contains(pos): return
		super().mouseReleaseEvent(evt)

	def mouseDoubleClickEvent(self, evt):
		if self.testClickBranchArrow(evt, True): return
		super().mouseDoubleClickEvent(evt)

	def mouseMoveEvent(self, evt):
		self.updateHoveredIndex(self.indexAt(evt.pos()))
		if self.dragEnabled(): super().mouseMoveEvent(evt)

	def leaveEvent(self, evt):
		super().leaveEvent(evt)
		self.updateHoveredIndex(None)

	def onScrollerValueChange(self, value):
		pos = self.mapFromGlobal(QCursor.pos())
		self.updateHoveredIndex(self.indexAt(pos))
		self.updateDropIndicatorRect(None)

	def _getCollapsedParent(self, index):
		parents = []
		parent = index.parent()
		while parent.isValid():
			parents.insert(0, parent)
			parent = parent.parent()
		for idx in parents:
			if not self.isExpanded(idx):
				return idx
	def keyPressEvent(self, evt):
		key = evt.key()
		mods = evt.modifiers()
		if key == Qt.Key_Right:
			# if self.underAnimating: return
			model = self.model()
			curr = self.currentIndex()
			if not curr.isValid():
				curr = model.index(0, 0, curr)
				if curr.isValid():
					self.toggleExpand(curr, mods & Qt.AltModifier)
					self.setCurrentIndex(curr)
				return

			curr = self.currentIndex()
			cp = self._getCollapsedParent(curr)
			if cp: return self.setCurrentIndex(cp)
			if not model.hasChildren(curr) or self.isExpanded(curr):
				while True:
					curr = self.indexBelow(curr)
					if not curr.isValid(): return
					if model.hasChildren(curr):
						self.setCurrentIndex(curr)
						return
			else:
				self.toggleExpand(curr, mods & Qt.AltModifier)

		elif key == Qt.Key_Left:
			# if self.underAnimating: return
			if not self.selectedIndexes(): return super().keyPressEvent(evt)
			model = self.model()
			curr = self.currentIndex()
			cp = self._getCollapsedParent(curr)
			if cp: return self.setCurrentIndex(cp)
			if not model.hasChildren(curr) or not self.isExpanded(curr):
				parent = curr.parent()
				if parent.isValid():
					self.setCurrentIndex(parent)
				else:
					row = curr.row()
					if row > 0: self.setCurrentIndex(curr.siblingAtRow(row - 1))
			else:
				self.toggleExpand(curr, mods & Qt.AltModifier)
		
		elif key == Qt.Key_Delete or (key == Qt.Key_Backspace and mods & Qt.ControlModifier):
			model = self.model()
			selections = self.selectionModel().selectedIndexes()
			selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and 1 or -1))
			for idx in selections: model.removeRow(idx.row(), idx.parent())

		elif key == Qt.Key_Escape:
			self.selectionModel().clear()

		elif key == Qt.Key_Space:
			curr = self.currentIndex()
			if not curr.isValid(): return
			overlay = TreeItemPingOverlay(self)
			overlay.startPing(curr)
			overlay.show()

		else:
			super().keyPressEvent(evt)

	def copySelection(self):
		model = self.model()
		selectionModel = self.selectionModel()
		selections = selectionModel.selectedIndexes()
		selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and -1 or 1))

		# detect children and remove
		for i in range(len(selections) - 1, 0, -1):
			curr = selections[i]
			for j in range(i - 1, -1, -1):
				test = selections[j]
				if isChildOfModelIndex(curr, test):
					del selections[i]
					break

		clipboard = QApplication.clipboard()
		clipboard.setMimeData(model.mimeData(selections))

	def pasteSelection(self):
		model = self.model()
		selectionModel = self.selectionModel()
		toSelections = []
		parent = self.currentIndex().parent()
		clipboard = QApplication.clipboard()
		oldRowCount = model.rowCount(parent)
		model.dropMimeData(clipboard.mimeData(), Qt.CopyAction, -1, -1, parent)
		newRowCount = model.rowCount(parent)
		dropedCount = newRowCount - oldRowCount
		if dropedCount > 0:
			selectionModel.clear()
			
			self.setCurrentIndex(model.index(newRowCount - 1, 0, parent))
			for i in range(newRowCount - dropedCount, newRowCount):
				selection = model.index(i, 0, parent)
				selectionModel.select(selection, QItemSelectionModel.Select)

			while parent.isValid():
				self.expandInstant(parent, False)
				parent = parent.parent()

		
	def duplicateSelection(self):
		model = self.model()
		selectionModel = self.selectionModel()
		selections = selectionModel.selectedIndexes()
		selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and -1 or 1))
		
		# detect children and remove
		for i in range(len(selections) - 1, 0, -1):
			curr = selections[i]
			for j in range(i - 1, -1, -1):
				test = selections[j]
				if isChildOfModelIndex(curr, test):
					del selections[i]
					break

		selectionModel.clear()
		toSelections = []
		for selection in selections:
			parent = selection.parent()
			mimeData = model.mimeData([selection])
			model.dropMimeData(mimeData, Qt.CopyAction, -1, -1, parent)

			row = model.rowCount(parent) - 1
			toSelections.append(model.index(row, 0, parent))

			while parent.isValid():
				self.expandInstant(parent, False)
				parent = parent.parent()

		self.setCurrentIndex(toSelections[-1])
		for selection in toSelections:
			selectionModel.select(selection, QItemSelectionModel.Select)

	def event(self, evt):
		super().event(evt)

		if evt.type() == QEvent.ShortcutOverride:
			key = evt.key()
			mods = evt.modifiers()

			if key == Qt.Key_A and mods & Qt.ControlModifier:
				self.keyPressEvent(evt)

			elif key == Qt.Key_C and mods & Qt.ControlModifier:
				self.copySelection()
			elif key == Qt.Key_V and mods & Qt.ControlModifier:
				self.pasteSelection()
			elif key == Qt.Key_D and mods & Qt.ControlModifier:
				self.duplicateSelection()


	##################  DRAW  ##################
	def paintEvent(self, event):
		painter = QPainter(self.viewport())
		painter.setClipping(True)
		self.drawTree(painter, event.region())
		painter.setClipping(False)
		self.drawDropIndicator(painter)

	def drawBranches(self, painter, rect, index):
		pass # skip default impl in QTreeView

	def drawDropIndicator(self, painter):
		if not self.dropAccepted: return
		if not self.dropIndicatorRect: return
		painter.setPen(self._penDropIndicator)
		l = self.dropIndicatorRect.left() + self.treePaddingLeft + 1 # indicatorOffset
		r = self.dropIndicatorRect.right()
		y = self.dropIndicatorRect.top()
		radius = 3
		painter.drawEllipse(l-2*radius, y-radius, 2*radius, 2*radius)
		painter.drawLine(l, y, r, y)

	def updateHoveredIndex(self, new):
		viewport = self.viewport()
		old = self.hoveredIndex
		if new != old:
			self.hoveredIndex = new
			if old:
				rect = self.visualRect(old)
				rect.setLeft(0)
				viewport.update(rect)
			if new:
				rect = self.visualRect(new)
				rect.setLeft(0)
				viewport.update(rect)

	def updateDropIndicatorRect(self, new):
		viewport = self.viewport()
		old = self.dropIndicatorRect
		if new != old:
			self.dropIndicatorRect = new
			w, h = self.width(), self.itemHeight
			if old:
				t = old.top() - round(h / 2)
				viewport.update(QRect(0, t, w, h))
			if new:
				t = new.top() - round(h / 2)
				viewport.update(QRect(0, t, w, h))


	##################  DRAG  ##################
	def startDrag(self, supportedActions):
		drag = QDrag(self)
		selections = self.selectedIndexes()
		drag.setMimeData(self.model().mimeData(selections))
		drag.exec(Qt.MoveAction)

	def dragEnterEvent(self, evt):
		self.dropAccepted = True
		evt.acceptProposedAction()

	def dragLeaveEvent(self, evt):
		self.updateDropIndicatorRect(None)
		self.updateHoveredIndex(None)

	def checkDropable(self, hovered, source):
		if source != self: return False
		if not hovered.isValid(): return True
		selectionModel = self.selectionModel()
		if selectionModel.isSelected(hovered): return False
		for select in selectionModel.selectedIndexes():
			# todo: check root index
			if isChildOfModelIndex(hovered, select): return False
		return True

	def dragMoveEvent(self, evt):
		pos = evt.pos()
		hovered = self.indexAt(pos)
		newDropIndicatorRect = None
		if hovered.isValid():
			rect = self.visualRect(hovered)
			y, l, t, b = pos.y(), rect.left(), rect.top(), rect.bottom()
			if y - t < self.dropIndicatorMargin: # and (y > margin and not self.hoveredIndex.isRoot())
				newDropIndicatorRect = QRect(l, t, self.width()-l, 0)
				self.dropPosition = -1
				self.autoExpandTimer.stop()

			elif b - y < self.dropIndicatorMargin:
				newDropIndicatorRect = QRect(l, b + 1, self.width()-l, 0)
				self.dropPosition = 1
				self.autoExpandTimer.stop()

			else:
				self.autoExpandTimer.start(400)
				self.dropPosition = 0

		src = evt.source()
		dropable = self.checkDropable(hovered, src)
		if self.dropAccepted != dropable:
			self.dropAccepted = dropable
			if dropable: evt.accept()
			else: evt.ignore()

		if not dropable: newDropIndicatorRect = None
		self.updateDropIndicatorRect(newDropIndicatorRect)
		self.updateHoveredIndex(hovered)
		if src != self: self.repaint()
		super().dragMoveEvent(evt)

	def dropEvent(self, evt):
		evt.acceptProposedAction()
		self.autoExpandTimer.stop()

		idx = self.indexAt(evt.pos())
		src = evt.source()
		if src == self:
			model = self.model()
			selectionModel = self.selectionModel()
			selections = selectionModel.selectedIndexes()
			selections.sort(key = functools.cmp_to_key(lambda e1, e2: isAboveOfModelIndex(e1, e2) and 1 or -1))
			selectionModel.clear()

			dropInsertRow, dropParent = None, None
			valid = idx.isValid()
			if valid and self.dropPosition == -1:
				dropInsertRow = idx.row()
				dropParent = idx.parent()
			elif valid and self.dropPosition == 1:
				dropInsertRow = idx.row() + 1
				dropParent = idx.parent()
			else:
				dropInsertRow = model.rowCount(idx)
				dropParent = idx

			delayRemoves = [selection for selection in selections if selection.parent() == dropParent and selection.row() < dropInsertRow]
			for selection in selections:
				mimeData = model.mimeData([selection])
				if selection not in delayRemoves: model.removeRow(selection.row(), selection.parent())
				model.dropMimeData(mimeData, Qt.CopyAction, dropInsertRow, -1, dropParent)

			dropCount = len(selections)
			self.setCurrentIndex(model.index(dropInsertRow + dropCount - 1, 0, dropParent))
			for i in range(dropInsertRow, dropInsertRow + dropCount): selectionModel.select(model.index(i, 0, dropParent), QItemSelectionModel.Select)
			
			for index in delayRemoves: model.removeRow(index.row(), index.parent())
			if valid and self.dropPosition == 0: self.expandInstant(idx, False)

			evt.acceptProposedAction()
		else:
			evt.ignore()

		self.updateDropIndicatorRect(None)


	################  ANIMATING  ################
	def toggleExpand(self, index, recursive):
		if self.isExpanded(index):
			def _collapse():
				if recursive:
					self._collapseRecursively(index)
				else:
					self.collapse(index)
			if self.customAnimated:
				self._playExpandAnim(index, True, recursive, _collapse)
			else:
				_collapse()
		else:
			if recursive:
				self.expandRecursively(index)
			else:
				self.expand(index)
			if self.customAnimated: self._playExpandAnim(index, False, recursive)

	def expandInstant(self, index, recursive):
		if self.isExpanded(index): return
		model = self.model()
		height = self.itemHeight
		list = self._animChildrenList(index, recursive)
		for idx in list: model.setData(idx, height, Qt.SizeHintRole)
		if recursive:
			self.expandRecursively(index)
		else:
			self.expand(index)

	def _collapseRecursively(self, index):
		self.collapse(index)
		model = self.model()
		count = model.rowCount(index)
		for r in range(count): self._collapseRecursively(model.index(r, 0, index))
	def _animChildrenList(self, index, includeHidden):
		list = []
		model = self.model()
		count = model.rowCount(index)
		for row in range(count):
			child = model.index(row, 0, index)
			list.append(child)
			if self.isExpanded(child) or includeHidden:
				list.extend(self._animChildrenList(child, includeHidden))
			# if model.hasChildren(child): list.extend(self._animChildrenList)
		return list
	def _playExpandAnim(self, index, collapse, recursive, onFinish = None):
		self.underAnimating = True
		self.animElapsed = 0
		self.prevIdxStop = 0
		self.reverseExpanding = collapse
		self.animIdxList = self._animChildrenList(index, recursive and not collapse)
		self.onAnimFinish = onFinish
		model = self.model()
		initHeight = 0
		if collapse:
			self.collapsingIndex = index
			self.animIdxList.reverse()
			initHeight = self.itemHeight
		for idx in self.animIdxList: model.setData(idx, initHeight, Qt.SizeHintRole)

		self.animTimer = QTimer()
		self.animTimer.timeout.connect(self._tickExpanding)
		self.animTimer.start(self._customAnimTickInterval)
		self.prevTickTime = time.time()

	def _tickExpanding(self):
		curr = time.time()
		delta = (curr - self.prevTickTime) * 1000
		self.prevTickTime = curr
		self.animElapsed += delta

		k = clamp(self.animElapsed / self.customAnimDuration, 0, 1)
		progress = easeInOutQuad(k)
		idxProgress = len(self.animIdxList) * progress
		idxStop = floor(idxProgress)
		
		resetHeight, currHeight = None, None
		if self.reverseExpanding:
			resetHeight, currHeight = 0, round((1 - idxProgress + idxStop) * self.itemHeight)
		else:
			resetHeight, currHeight = self.itemHeight, round((idxProgress - idxStop) * self.itemHeight)

		model = self.model()
		if progress < 1:
			for i in range(self.prevIdxStop, idxStop): model.setData(self.animIdxList[i], resetHeight, Qt.SizeHintRole)
			model.setData(self.animIdxList[idxStop], currHeight, Qt.SizeHintRole)
			self.prevIdxStop = idxStop
			# model.dataChanged.emit(self.animIdxList[self.prevIdxStop], self.animIdxList[self.idxStop], [Qt.SizeHintRole])
		else:
			for i in range(self.prevIdxStop, len(self.animIdxList)): model.setData(self.animIdxList[i], self.itemHeight, Qt.SizeHintRole)
			# model.setData(self.animIdxList[-1], self.itemHeight, Qt.SizeHintRole)
			self.underAnimating = False
			self.animTimer.stop()
			self.animTimer.deleteLater()
			self.animElapsed = None
			self.animIdxList = None
			self.prevIdxStop = None
			self.prevTickTime = None
			self.collapsingIndex = None
			if self.onAnimFinish:
				self.onAnimFinish()
				self.onAnimFinish = None

	def expandHovered(self):
		if not self.hoveredIndex or not self.hoveredIndex.isValid(): return
		if not self.model().hasChildren(self.hoveredIndex): return
		for selection in self.selectedIndexes():
			if self.hoveredIndex == selection: return
			if isChildOfModelIndex(self.hoveredIndex, selection): return
		if self.isExpanded(self.hoveredIndex): return
		self.toggleExpand(self.hoveredIndex, False)
		# self.expandInstant(self.hoveredIndex, False)

	def pingItem(self, index):
		pass


	####################  UTILS  ####################
	def _rowCountRecursive(self, index, model):
		count = model.rowCount(index)
		for row in range(count): count += self._rowCountRecursive(model.index(row, 0, index), model)
		return count
	def _flatRowNumber(self, index, model):
		if not index.isValid(): return -1
		result = index.row() + 1
		parent = index.parent()
		for row in range(result - 1): result += self._rowCountRecursive(model.index(row, 0, parent), model)
		return result + self._flatRowNumber(parent, model)

	def _visibleRowCountRecursive(self, index, model):
		count = model.rowCount(index)
		if not self.isExpanded(index) or self.collapsingIndex == index: return 0
		for row in range(count): count += self._visibleRowCountRecursive(model.index(row, 0, index), model)
		return count
	def _flatVisibleRowNumber(self, index, model):
		if not index.isValid(): return -1
		result = index.row() + 1
		parent = index.parent()
		for row in range(result - 1): result += self._visibleRowCountRecursive(model.index(row, 0, parent), model)
		return result + self._flatVisibleRowNumber(parent, model)

