from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QBrush, QFontMetrics, QPen, QPalette
from PySide6.QtWidgets import QProxyStyle, qDrawShadeRect, qDrawPlainRect, QStyleOptionMenuItem, QMenu
from editor.common.icon_cache import getThemePixmap

class MenuStyleMacOS(QProxyStyle):
	def __init__(self, conf = None):
		super().__init__()
		self.conf = conf or {}

	def border(self):
		return self.conf['border'] if 'border' in self.conf else Qt.transparent
	def borderWidth(self):
		return self.conf['borderWidth'] if 'borderWidth' in self.conf else 1
	def borderRadius(self):
		return self.conf['borderRadius'] if 'borderRadius' in self.conf else 6

	def background(self):
		return self.conf['background'] if 'background' in self.conf else QColor('#e8e8e8')
	def backgroundHovered(self):
		return self.conf['backgroundHovered'] if 'backgroundHovered' in self.conf else QColor('#498afd')
	def text(self):
		return self.conf['text'] if 'text' in self.conf else QColor('#222')
	def textHovered(self):
		return self.conf['textHovered'] if 'textHovered' in self.conf else QColor('#fff')
	def shortcut(self):
		return self.conf['shortcut'] if 'shortcut' in self.conf else QColor('#aaa')
	def separator(self):
		return self.conf['separator'] if 'separator' in self.conf else QColor('#bbb')

	def contentPadding(self):
		return self.conf['contentPadding'] if 'contentPadding' in self.conf else 15
	def checkedPadding(self):
		return self.conf['checkedPadding'] if 'checkedPadding' in self.conf else 10

	def itemBackgroundPadding(self):
		return self.conf['itemBackgroundPadding'] if 'itemBackgroundPadding' in self.conf else 5
	def itemBackgroundRadius(self):
		return self.conf['itemBackgroundRadius'] if 'itemBackgroundRadius' in self.conf else 4

	def itemHeight(self):
		return self.conf['itemHeight'] if 'itemHeight' in self.conf else 22
	def separatorHeight(self):
		return self.conf['separatorHeight'] if 'separatorHeight' in self.conf else 1
	def separatorVSpacing(self):
		return self.conf['separatorVSpacing'] if 'separatorVSpacing' in self.conf else 4

	def subMenuOverlap(self):
		return self.conf['subMenuOverlap'] if 'subMenuOverlap' in self.conf else 5
	def fontSize(self):
		return self.conf['fontSize'] if 'fontSize' in self.conf else 12

	def submenuIcon(self):
		return self.conf['submenuIcon'] if 'submenuIcon' in self.conf else 'submenu.png'
	def submenuIconHovered(self):
		return self.conf['submenuIconHovered'] if 'submenuIconHovered' in self.conf else 'submenu2.png'
	def submenuIconSize(self):
		return self.conf['submenuIconSize'] if 'submenuIconSize' in self.conf else 12
	def submenuIconOffsetX(self):
		return self.conf['submenuIconOffsetX'] if 'submenuIconOffsetX' in self.conf else 2
	def submenuIconOffsetY(self):
		return self.conf['submenuIconOffsetY'] if 'submenuIconOffsetY' in self.conf else 1

	def checkedIcon(self):
		return self.conf['checkedIcon'] if 'checkedIcon' in self.conf else 'check.png'
	def checkedIconHovered(self):
		return self.conf['checkedIconHovered'] if 'checkedIconHovered' in self.conf else 'check2.png'
	def checkedIconSize(self):
		return self.conf['checkedIconSize'] if 'checkedIconSize' in self.conf else 12
	def checkedIconOffsetX(self):
		return self.conf['checkedIconOffsetX'] if 'checkedIconOffsetX' in self.conf else -1
	def checkedIconOffsetY(self):
		return self.conf['checkedIconOffsetY'] if 'checkedIconOffsetY' in self.conf else 1
	
	def menuScrollerIcon(self):
		return self.conf['menuScrollerIcon'] if 'menuScrollerIcon' in self.conf else 'submenu.png'
	
	
	def pixelMetric(self, metric, option, widget):
		if metric == self.PM_SubMenuOverlap: return -self.subMenuOverlap();
		return super().pixelMetric(metric, option, widget)

	def hasCheckedAction(self, widget):
		for action in widget.actions():
			if action.isChecked():
				return True
		return False

	def sizeFromContents(self, contentsType, option, size, widget):
		size = super().sizeFromContents(contentsType, option, size, widget)
		if contentsType == self.CT_MenuItem:
			menuItem = option
			menuItem.__class__ = QStyleOptionMenuItem
			mtype = menuItem.menuItemType
			if mtype == QStyleOptionMenuItem.Separator:
				size.setHeight(self.separatorHeight() + self.separatorVSpacing() * 2)
			else:
				size.setHeight(self.itemHeight())
				if menuItem.checked: size.setWidth(size.width() + self.checkedPadding())
				if mtype == QStyleOptionMenuItem.SubMenu: size.setWidth(size.width() + self.contentPadding())
				tabIdx = menuItem.text.find('\t')
				if tabIdx >= 0:
					shortcutText = menuItem.text[tabIdx+1:]
					
					font = menuItem.font
					font.setPixelSize(self.fontSize())
					font.setFamily('.AppleSystemUIFont')
					newWidth = QFontMetrics(font).horizontalAdvance(shortcutText)
					oldWidth = menuItem.fontMetrics.horizontalAdvance(shortcutText)

					size.setWidth(size.width() + self.contentPadding() + newWidth - oldWidth)
		return size

	def drawControl(self, element, option, painter, widget):
		if element == self.CE_MenuScroller or element == self.CE_MenuTearoff:
			rect = option.rect
			center = rect.center()
			cx, cy = center.x(), center.y()
			w, h = rect.width(), rect.height()
			iconSize = self.submenuIconSize()
			iconRect = QRect(cx - iconSize / 2, cy - iconSize / 2, iconSize, iconSize)
			down = option.state & self.State_DownArrow
			
			painter.save()
			painter.translate(iconRect.center())
			painter.rotate(90 if down else -90)
			painter.translate(-iconRect.center())
			painter.drawPixmap(iconRect, getThemePixmap(self.menuScrollerIcon()))
			painter.restore()

		elif element == self.CE_MenuItem:
			menuItem = option
			menuItem.__class__ = QStyleOptionMenuItem
			painter.save()

			hovered = menuItem.state & self.State_Selected and menuItem.state & self.State_Enabled
			if hovered:
				radius = self.itemBackgroundRadius()
				padding = self.itemBackgroundPadding()
				painter.setPen(Qt.transparent)
				painter.setBrush(self.backgroundHovered())
				painter.drawRoundedRect(menuItem.rect.adjusted(padding, 0, -padding, 0), radius, radius)

			contentPadding = self.contentPadding()
			checkedPadding = self.checkedPadding()
			textLeftPadding = contentPadding
			if self.hasCheckedAction(widget): textLeftPadding += checkedPadding 

			rect = menuItem.rect
			mtype = menuItem.menuItemType
			if mtype == QStyleOptionMenuItem.Separator:
				y, r = rect.y(), rect.right()
				separatorRect = QRect(contentPadding, y + self.separatorVSpacing(), r - contentPadding * 2, self.separatorHeight())
				painter.fillRect(separatorRect, self.separator())

			if mtype == QStyleOptionMenuItem.TearOff:
				print(1)

			elif mtype == QStyleOptionMenuItem.SubMenu:
				textRect = menuItem.rect
				textRect.moveLeft(textLeftPadding)
				textFlags = Qt.AlignVCenter | Qt.TextShowMnemonic | Qt.TextDontClip | Qt.TextSingleLine
				font = menuItem.font
				font.setPixelSize(self.fontSize())
				painter.setFont(font)
				painter.setPen(self.textHovered() if hovered else self.text())
				painter.drawText(textRect, textFlags, menuItem.text)
				
				y, w, h = rect.center().y(), rect.width(), rect.height()
				iconSize = self.submenuIconSize()
				offsetX, offsetY = self.submenuIconOffsetX(), self.submenuIconOffsetY()
				iconRect = QRect(w - iconSize - contentPadding + offsetX, y - iconSize / 2 + offsetY, iconSize, iconSize)
				iconPath = self.submenuIconHovered() if hovered else self.submenuIcon()
				painter.drawPixmap(iconRect, getThemePixmap(iconPath))

			else:
				if menuItem.checked:
					y, w, h = rect.center().y(), rect.width(), rect.height()
					iconSize = self.checkedIconSize()
					offsetX, offsetY = self.checkedIconOffsetX(), self.checkedIconOffsetY()
					iconRect = QRect(contentPadding - iconSize / 2 + offsetX, y - iconSize / 2 + offsetY, iconSize, iconSize)
					iconPath = self.checkedIconHovered() if hovered else self.checkedIcon()
					painter.drawPixmap(iconRect, getThemePixmap(iconPath))

				font = menuItem.font
				font.setPixelSize(self.fontSize())
				themeFontFamily = font.family()
				textFlags = Qt.AlignVCenter | Qt.TextShowMnemonic | Qt.TextDontClip | Qt.TextSingleLine
				tabIdx = menuItem.text.find('\t')
				hasShortcut = tabIdx >= 0
				label = menuItem.text[:tabIdx] if hasShortcut else menuItem.text
				if hasShortcut:
					shortcutText = menuItem.text[tabIdx+1:]
					painter.setPen(self.textHovered() if hovered else self.shortcut())
					font.setFamily('.AppleSystemUIFont')
					fm = QFontMetrics(font)
					width = fm.horizontalAdvance(shortcutText)
					y, r, h = rect.y(), rect.right(), rect.height()
					shortcutRect = QRect(r - width - contentPadding, y, width, h)
					painter.setFont(font)
					painter.drawText(shortcutRect, textFlags | Qt.AlignRight, shortcutText)
				textRect = menuItem.rect
				textRect.moveLeft(textLeftPadding)
				font.setFamily(themeFontFamily)
				painter.setFont(font)
				painter.setPen(self.textHovered() if hovered else self.text())
				painter.drawText(textRect, textFlags, label)

			painter.restore()

		else:
			super().drawControl(element, option, painter, widget)

	def drawPrimitive(self, element, option, painter, widget):
		# if element == self.PE_FrameMenu: #menu frame, when frame width > 0
		# 	qDrawShadeRect(painter, option.rect, option.palette, option.state & self.State_Sunken, 1, 0, self.border())

		if element == self.PE_PanelMenu: # menu background
			painter.setRenderHint(QPainter.Antialiasing, True)
			painter.setRenderHint(QPainter.TextAntialiasing, True)
			painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
			
			radius = self.borderRadius()
			width = self.borderWidth()

			painter.setBrush(self.border())
			painter.setPen(Qt.transparent)
			painter.drawRoundedRect(option.rect, radius, radius)

			radius -= width
			painter.setBrush(self.background())
			painter.drawRoundedRect(option.rect.adjusted(width, width, -width, -width), radius, radius)
			# qDrawPlainRect(painter, option.rect, self.border(), self.borderWidth(), QBrush(self.background()))
		else:
			super().drawPrimitive(element, option, painter, widget)

	def polish(self, widget):
		super().polish(widget)
		if not isinstance(widget, QMenu): return
		if widget.windowFlags() & Qt.FramelessWindowHint: return
		widget.setWindowFlag(Qt.FramelessWindowHint, True)


class MenuStyleWindows(QProxyStyle):
	def drawControl(self, element, option, painter, widget):
		if element != self.CE_MenuItem: return super().drawControl(element, option, painter, widget)

		menuItem = option
		menuItem.__class__ = QStyleOptionMenuItem
		mtype = menuItem.menuItemType
		if mtype != QStyleOptionMenuItem.Normal: return super().drawControl(element, option, painter, widget)
		textParts = option.text.split('\t')
		if len(textParts) == 1: return super().drawControl(element, option, painter, widget)

		option.text = textParts[0]
		super().drawControl(element, option, painter, widget)
		textFlags = Qt.AlignRight | Qt.AlignVCenter | Qt.TextShowMnemonic | Qt.TextDontClip | Qt.TextSingleLine
		self.drawItemText(painter, option.rect.adjusted(0, 0, -10, 0), textFlags, option.palette, option.state & self.State_Enabled, textParts[1], QPalette.Text)

