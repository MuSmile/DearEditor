# from PySide6.QtCore import Qt
# from PySide6.QtGui import QPainter, QColor, QBrush
# from PySide6.QtWidgets import QProxyStyle
# from editor.common.util import getIde


# class ProxyStyle(QProxyStyle):
# 	def drawControl(self, element, option, painter, widget):
# 		# print(element)
# 		if element == self.CE_PushButtonLabel: return
# 		super().drawControl(element, option, painter, widget)

# 	def drawPrimitive(self, element, option, painter, widget):
# 		# print(element)
# 		super().drawPrimitive(element, option, painter, widget)

# 	def drawComplexControl(self, control, option, painter, widget):
# 		# print(control)
# 		super().drawComplexControl(control, option, painter, widget)

# 	def sizeFromContents(self, contentsType, option, contentsSize, widget):
# 		contentsSize = super().sizeFromContents(contentsType, option, contentsSize, widget)
# 		# print(contentsType)
# 		if contentsType == self.CT_PushButton: contentsSize.rwidth += 20;
# 		return contentsSize;


# getIde().setStyle(ProxyStyle())