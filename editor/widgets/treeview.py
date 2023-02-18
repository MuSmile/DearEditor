from math import floor
from PySide6.QtCore import Qt, Property, QSize, QRect, QTimer, QPointF
from PySide6.QtWidgets import QTreeView, QApplication, QAbstractItemView, QItemDelegate, QStyle
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPen, QBrush, QPainter, QColor, QDrag, QCursor, QPixmap, QMouseEvent
from editor.common.math import clamp
from editor.common.ease import easeInOutQuad
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

	# def createEditor(self, parent, option, index):
	# 	w = super().createEditor(parent, option, index)
	# 	QTimer.singleShot(1, lambda: w.move(option.rect.x() + 22, w.pos().y()))
	# 	return w

	def paint(self, painter, option, index):
		painter.setRenderHint(QPainter.Antialiasing)

		view = self.view
		rect = option.rect
		rect.setHeight(view.itemHeight)

		l, r = rect.left(), rect.right() + 1
		t, h = rect.top(), rect.height()

		self.drawBackground(painter, QRect(0, t, r, h), option.state, index)
		self.drawBranches(painter, QRect(0, t, l, h), index)
		self.drawContent(painter, rect, index)

	def drawBackground(self, painter, rect, state, index):
		selected = state & QStyle.State_Selected
		hovered  = index == self.view.hoveredIndex # option.state & QStyle.State_MouseOver
		bgColor  = None
		if selected:
			bgColor = QColor('#515c84')
		elif hovered:
			bgColor = QColor('#454768')
		else:
			# alternate = option.features & QStyleOptionViewItem.Alternate
			alternate = self._flatVisibleRowNumber(index, self.view.model()) % 2
			bgColor = alternate and QColor('#404040') or QColor('#474747')
		painter.fillRect(rect, bgColor)
	def drawContent(self, painter, rect, index):
		view = self.view
		textOffset = view.paddingLeft
		decoration = index.data(Qt.DecorationRole)

		if decoration:
			indentation = view.indentation()
			rectSize = view.itemHeight
			textOffset += indentation + 2
			cx, cy = rect.left() + round(indentation / 2), rect.top() + round(rect.height() / 2)
			iconSize, halfSize = 16, 8
			x, y = cx - halfSize, cy - halfSize
			iconOffset = round((rectSize - iconSize) / 2) + view.paddingLeft - 2
			painter.drawPixmap(x + iconOffset, y, iconSize, iconSize, decoration)

		painter.drawText(rect.adjusted(textOffset, -1, 0, 0), Qt.AlignVCenter, index.data())
	
	def drawBranches(self, painter, rect, index):
		view = self.view
		filterDepth = 1
		itemDepth = self._depth(index)
		drawDepth = itemDepth - filterDepth
		if drawDepth >= 0:
			painter.setOpacity(0.4)
			indentation = view.indentation()
			t, h = rect.top(), rect.height()
			# print(index.siblingAtRow(index.row()+1).isValid(), index.data())
			curr = index
			for i in range(drawDepth):
				x = int(indentation * (itemDepth - i - 0.5)) + view.paddingLeft
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
		self.drawBranchArrow(painter, rect, index)
	def drawBranchArrow(self, painter, rect, index):
		if not index.model().hasChildren(index): return

		view = self.view
		size, sizeHalf = 12, 6
		cx = rect.right() - round(view.indentation() / 2) + 1 + view.paddingLeft
		cy = rect.top() + (rect.height() / 2)
		rect = QRect(cx - sizeHalf, cy - sizeHalf, size, size)
		branchArrow = view.isExpanded(index) and view.branchOpened or view.branchClosed
		painter.drawPixmap(rect, branchArrow)

	####################  UTILS  ####################
	def _depth(self, index):
		depth = 0
		parent = index.parent()
		while parent.isValid():
			depth += 1
			parent = parent.parent()
		return depth
		
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
		if not self.view.isExpanded(index) or self.view.collapsingIndex == index: return 0
		for row in range(count): count += self._visibleRowCountRecursive(model.index(row, 0, index), model)
		return count
	def _flatVisibleRowNumber(self, index, model):
		if not index.isValid(): return -1
		result = index.row() + 1
		parent = index.parent()
		for row in range(result - 1): result += self._visibleRowCountRecursive(model.index(row, 0, parent), model)
		return result + self._flatVisibleRowNumber(parent, model)
			
class TreeView(QTreeView):
	@Property(int)
	def paddingLeft(self):
		return self._paddingLeft
	@paddingLeft.setter
	def paddingLeft(self, value):
		if self._paddingLeft == value: return
		self._paddingLeft = value
		self.repaint()

	@Property(int)
	def itemHeight(self):
		return self._itemHeight
	@itemHeight.setter
	def itemHeight(self, value):
		if self._itemHeight == value: return
		self._itemHeight = value
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
	
	def __init__(self, parent = None):
		super().__init__(parent)
		self._paddingLeft = 2
		self._penDropIndicator = QPen(QColor('#8af'), 2)
		self._pixmapBranchOpened = getThemePixmap('arrow_down.png')
		self._pixmapBranchClosed = getThemePixmap('arrow_right.png')
		self._customAnimated = True
		self._customAnimDuration = 120
		self._customAnimTickInterval = 10
		self._dropIndicatorMargin = 5
		self._itemHeight = 20
		self.setIndentation(20)

		self.hoveredIndex = None
		self.underAnimating = None
		self.collapsingIndex = None
		self.dropIndicatorRect = None
		
		self.setMouseTracking(True)
		self.setItemDelegate(TreeItemDelegate(self))

		self.setAnimated(False)
		self.setHeaderHidden(True)
		self.setAlternatingRowColors(False)
		self.setExpandsOnDoubleClick(False)

		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setDragDropMode(QAbstractItemView.InternalMove)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

		self.setEditTriggers(QAbstractItemView.SelectedClicked)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		# self.verticalScrollBar().setSingleStep(5)


	#################  EVENTS  #################
	def testClickBranchArrow(self, evt):
		if self.underAnimating: return True
		pos = evt.pos()
		index = self.indexAt(pos)
		if not self.model().hasChildren(index): return False
		rect = self.visualRect(index)
		l, t, h = rect.left(), rect.top(), rect.height()
		indentation = self.indentation()
		branchRect = QRect(l - indentation + self.paddingLeft, t, indentation, h)
		if branchRect.contains(pos):
			recursive = evt.modifiers() == Qt.AltModifier
			self.toggleExpand(index, recursive)
			return True

	def mousePressEvent(self, evt):
		if self.testClickBranchArrow(evt): return
		super().mousePressEvent(evt)

	def mouseReleaseEvent(self, evt):
		pos = evt.pos()
		index = self.indexAt(pos)
		rect = self.visualRect(index)
		l, t, h = rect.left(), rect.top(), rect.height()
		indentation = self.indentation()
		branchRect = QRect(l - indentation + self.paddingLeft, t, indentation, h)
		if branchRect.contains(pos): return
		super().mouseReleaseEvent(evt)

	def mouseDoubleClickEvent(self, evt):
		if self.testClickBranchArrow(evt): return
		super().mouseDoubleClickEvent(evt)

	def mouseMoveEvent(self, evt):
		super().mouseMoveEvent(evt)
		self.hoveredIndex = self.indexAt(evt.pos())

	def wheelEvent(self, evt):
		super().wheelEvent(evt)
		pos = self.mapFromGlobal(QCursor.pos())
		self.hoveredIndex = self.indexAt(pos)

	def paintEvent(self, event):
		painter = QPainter(self.viewport())
		self.drawTree(painter, event.region())
		self.drawDropIndicator(painter)

	def drawBranches(self, painter, rect, index):
		pass

	def drawDropIndicator(self, painter):
		if not self.dropIndicatorRect: return
		painter.setPen(self._penDropIndicator)
		l = self.dropIndicatorRect.left() + self.paddingLeft + 2 # indicatorOffset
		r = self.dropIndicatorRect.right()
		y = self.dropIndicatorRect.top()
		radius = 3
		painter.drawEllipse(l-2*radius, y-radius, 2*radius, 2*radius)
		painter.drawLine(l, y, r, y)


	##################  DRAG  ##################
	def startDrag(self, supportedActions):
		drag = QDrag(self)
		selections = self.selectedIndexes()
		drag.setMimeData(self.model().mimeData(selections))
		if drag.exec(Qt.MoveAction) == Qt.MoveAction:
			model = self.model()
			for selection in selections:
				model.removeRows(selection.row(), 1, selection.parent())

	def dragEnterEvent(self, evt):
		print('dragEnterEvent')
		evt.acceptProposedAction()

	def dragLeaveEvent(self, evt):
		print('dragLeaveEvent')
		if self.dropIndicatorRect:
			self.dropIndicatorRect = None
			self.repaint()

	def dragMoveEvent(self, evt):
		super().dragMoveEvent(evt)
		newDropIndicatorRect = None

		pos = evt.pos()
		hovered = self.indexAt(pos)
		if hovered.isValid():
			if self.hoveredIndex != hovered:
				self.update(hovered)
				self.update(self.hoveredIndex)
				self.hoveredIndex = hovered

			rect = self.visualRect(hovered)
			y, l, t, b = pos.y(), rect.left(), rect.top(), rect.bottom()
			if y - t < self.dropIndicatorMargin: # and (y > margin and not self.hoveredItem.isRoot())
				newDropIndicatorRect = QRect(l, t, self.width()-l, 0)
			elif b - y < self.dropIndicatorMargin:
				newDropIndicatorRect = QRect(l, b + 1, self.width()-l, 0)
		
		if self.dropIndicatorRect != newDropIndicatorRect:
			self.dropIndicatorRect = newDropIndicatorRect
			self.repaint()

	def dropEvent(self, evt):
		print('dropEvent')
		idx = self.indexAt(evt.pos())
		if not idx.isValid(): return print('wtf')
		self.model().dropMimeData(evt.mimeData(), Qt.MoveAction, -1, -1, idx)
		evt.acceptProposedAction()


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
	def _tickExpanding(self):
		self.animElapsed += self.customAnimTickInterval
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
			model.setData(self.animIdxList[-1], self.itemHeight, Qt.SizeHintRole)
			self.underAnimating = False
			self.animTimer.stop()
			self.animTimer.deleteLater()
			self.animElapsed = None
			self.animIdxList = None
			self.prevIdxStop = None
			self.collapsingIndex = None
			if self.onAnimFinish:
				self.onAnimFinish()
				self.onAnimFinish = None


def runTreeDemo():
	view = TreeView(QApplication.activeWindow())
	view.setWindowFlags(Qt.Window)
	model = QStandardItemModel()
	for i in range(5):
		n = QStandardItem(f'Item_{i}')
		n.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
		model.appendRow(n)
		for j in range(4):
			c = QStandardItem(f'Child_{j}')
			c.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
			n.appendRow(c)
			for k in range(4):
				s = QStandardItem(f'Subchild_{k}')
				# s.setData(getThemePixmap('entity.png').scaled(16, 16), Qt.DecorationRole)
				c.appendRow(s)

	# model.dataChanged.connect(lambda i1, i2, r: print(r))
	view.setModel(model)

	view.setStyleSheet('''
		TreeView
		{
		    background: #444;
		    color: #fff;
		}
	''')

	view.show()
