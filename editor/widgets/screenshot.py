import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from editor.tools.util import clamp
from editor.view_manager import *

_saveDir = '.screenshots'
_saveName = format(QDateTime().currentDateTime().toString("yyyyMMdd-hhmmss"))
_saveFormat = 'png'

_labelFont = QFont('consolas', 8)
_borderPen = QPen(QColor('#080'))
_borderBrush = QBrush(QColor('#080'))

def takeScreenshot(self):
    if Screenshot.Instance: return
    Screenshot().show()

class Screenshot(QWidget):
    Instance = None
    Unselected, Selecting, Reselecting, Selected = range(4)

    def __init__(self):
        super().__init__(QApplication.activeWindow())
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(QApplication.primaryScreen().virtualGeometry())
        self.setMouseTracking(True)
        self.state = self.Unselected
        self.mouseMoved = False
        Screenshot.Instance = self

        self.screen = self.grabScreen()
        self.screenImg = self.screen.toImage()
        self.selection = None
        self.reselectable = False
        self.mask = QPixmap(self.size())
        self.maskClearColor = QColor(0, 0, 0, 128)
        self.updateMask()
        # self.save(screen)

    def grabScreen(self):
        final = QPixmap(self.size())
        # final.fill(Qt.white)
        painter = QPainter(final)
        for screen in QApplication.screens():
            rect = screen.geometry()
            screenshot = screen.grabWindow()
            painter.drawPixmap(rect, screenshot)
        return final

    def updateMask(self):
        self.mask.fill(self.maskClearColor)
        if self.selection == None: return
        painter = QPainter(self.mask)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(self.selection, Qt.transparent)

    def save(self):
        if self.selection == None: return
        if not os.path.isdir(_saveDir): os.makedirs(_saveDir)
        pixmap = self.screen.copy(self.selection)
        pixmap.save(f'{_saveDir}/{_saveName}.{_saveFormat}')
        self.close()

    def saveAs(self):
        if self.selection == None: return
        file = QFileDialog.getSaveFileName(self, 'Save Screenshot', '', 'Images (*.png *.jpg)')[0]
        if not file: return
        pixmap = self.screen.copy(self.selection)
        pixmap.save(file)
        self.close()

    def keyPressEvent(self, evt):
        key = evt.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.save()
        elif key == Qt.Key_S:
            self.saveAs()

    def clearOverrideCursor(self):
        while QApplication.overrideCursor(): QApplication.restoreOverrideCursor()

    def checkSizeGripHoverd(self, pos, force = False):
        if self.selection == None: return
        if force: self.reselectable = False

        boundingRect = self.selection.adjusted(-2, -2, 2, 2)
        if not boundingRect.contains(pos):
            if self.reselectable:
                self.reselectable = False
                self.clearOverrideCursor()
            return

        p0 = self.selection.topLeft()
        p1 = self.selection.bottomLeft()
        p2 = self.selection.bottomRight()
        p3 = self.selection.topRight()
        w, h = self.selection.width(), self.selection.height()
        inside = lambda center: abs(pos.x()-center.x()) <= 2 and abs(pos.y()-center.y()) <= 2
        if w == 0 and h == 0:
            if self.reselectable == 'rezise_all': return
            self.reselectable = 'rezise_all'
            self.anchorX, self.anchorY = p0.x(), p0.y()
            QGuiApplication.setOverrideCursor(Qt.SizeFDiagCursor)
        elif w == 0:
            if inside(p1):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p0.x(), p0.y()
                QGuiApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            elif inside(p0):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p1.x(), p1.y()
                QGuiApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            else:
                if self.reselectable == 'rezise_hor': return
                self.reselectable = 'rezise_hor'
                self.anchorX = p0.x()
                QGuiApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif h == 0:
            if inside(p2):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p1.x(), p1.y()
                QGuiApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            elif inside(p1):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p2.x(), p2.y()
                QGuiApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            else:
                if self.reselectable == 'rezise_ver': return
                self.reselectable = 'rezise_ver'
                self.anchorY = p1.y()
                QGuiApplication.setOverrideCursor(Qt.SizeVerCursor)
        else:
            if self.selection.adjusted(2, 2, -2, -2).contains(pos):
                if self.reselectable != 'move':
                    self.reselectable = 'move'
                    self.anchorX, self.anchorY = p0.x(), p0.y()
                    QGuiApplication.setOverrideCursor(Qt.SizeAllCursor)
                return

            if inside(p2):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p0.x(), p0.y()
                QGuiApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            elif inside(p1):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p3.x(), p3.y()
                QGuiApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            elif inside(p0):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p2.x(), p2.y()
                QGuiApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            elif inside(p3):
                if self.reselectable == 'rezise_all': return
                self.reselectable = 'rezise_all'
                self.anchorX, self.anchorY = p1.x(), p1.y()
                QGuiApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            else:
                ty, by = p0.y(), p1.y()
                lx, rx = p1.x(), p2.x()
                x, y = pos.x(), pos.y()
                if abs(x - lx) <= 2:
                    if self.reselectable == 'rezise_hor': return
                    self.reselectable = 'rezise_hor'
                    self.anchorX = rx
                    QGuiApplication.setOverrideCursor(Qt.SizeHorCursor)
                elif abs(x - rx) <= 2:
                    if self.reselectable == 'rezise_hor': return
                    self.reselectable = 'rezise_hor'
                    self.anchorX = lx
                    QGuiApplication.setOverrideCursor(Qt.SizeHorCursor)
                elif abs(y - ty) <= 2:
                    if self.reselectable == 'rezise_ver': return
                    self.reselectable = 'rezise_ver'
                    self.anchorY = by
                    QGuiApplication.setOverrideCursor(Qt.SizeVerCursor)
                else:
                    if self.reselectable == 'rezise_ver': return
                    self.reselectable = 'rezise_ver'
                    self.anchorY = ty
                    QGuiApplication.setOverrideCursor(Qt.SizeVerCursor)

    def mousePressEvent(self, evt):
        btn = evt.button()
        if btn == Qt.RightButton: return
        if btn == Qt.MiddleButton: return evt.ignore()
        pos = evt.pos()
        self.mouseDownPos = pos
        self.mouseMoved = False
        self.checkSizeGripHoverd(pos, True)

        if self.state == self.Unselected:
            self.state = self.Selecting
            self.selection = QRect(pos, pos)
        elif self.reselectable:
            self.state = self.Reselecting

    def mouseReleaseEvent(self, evt):
        btn = evt.button()
        if btn == Qt.RightButton:
            if self.state == self.Unselected:
                self.close()
            else:
                self.selection = None
                self.reselectable = False
                self.state = self.Unselected
                self.clearOverrideCursor()
                self.updateMask()
                self.update()
            return
        if btn == Qt.MiddleButton: return evt.ignore()

        if self.state == self.Unselected: return
        if self.state == self.Selecting and not self.mouseMoved:
            self.state = self.Selected
            pos = evt.pos()

            for dc in getDockManager().dockContainers():
                win = dc.parent()
                rect = win.frameGeometry()
                if not rect.contains(pos): continue

                self.selection = rect
                gp = dc.mapToGlobal(-dc.geometry().topLeft())
                rect = dc.geometry().translated(gp)
                if rect.contains(pos):
                    area = dc.dockAreaAt(pos)
                    if area:
                        gp = area.mapToGlobal(-area.pos())
                        self.selection = area.geometry().translated(gp)
                    else:
                        self.selection = rect

                self.updateMask()
                self.update()
                return

            self.selection = QApplication.screenAt(pos).geometry()
            self.updateMask()
            self.update()

        elif self.state != self.Selected:
            self.state = self.Selected
            self.checkSizeGripHoverd(evt.pos())
            self.update()

    def mouseMoveEvent(self, evt):
        pos = evt.pos()
        if not self.mouseMoved: self.mouseMoved = True
        if self.state == self.Selected: return self.checkSizeGripHoverd(pos)
        if self.state == self.Unselected:
            pass
        elif self.state == self.Selecting:
            x1, y1 = pos.x(), pos.y()
            x0, y0 = self.mouseDownPos.x(), self.mouseDownPos.y()
            x, y = min(x0, x1), min(y0, y1)
            w, h = abs(x0 - x1) + 1, abs(y0 - y1) + 1
            self.selection.setRect(x, y, w, h)
            self.updateMask()
        elif self.state == self.Reselecting:
            dm = pos - self.mouseDownPos
            dx, dy = dm.x(), dm.y()
            if self.reselectable == 'move':
                x = clamp(self.anchorX + dx, 0, self.screen.width() - self.selection.width())
                y = clamp(self.anchorY + dy, 0, self.screen.height() - self.selection.height())
                self.selection.moveTo(x, y)
                self.updateMask()
            elif self.reselectable == 'rezise_all':
                x1, y1 = pos.x(), pos.y()
                x0, y0 = self.anchorX, self.anchorY
                x, y = min(x0, x1), min(y0, y1)
                w, h = abs(x0 - x1) + 1, abs(y0 - y1) + 1
                self.selection.setRect(x, y, w, h)
                self.updateMask()
            elif self.reselectable == 'rezise_hor':
                x1 = pos.x()
                x0 = self.anchorX
                x = min(x0, x1)
                w = abs(x0 - x1) + 1
                self.selection.setX(x)
                self.selection.setWidth(w)
                self.updateMask()
            elif self.reselectable == 'rezise_ver':
                y1 = pos.y()
                y0 = self.anchorY
                y = min(y0, y1)
                h = abs(y0 - y1) + 1
                self.selection.setY(y)
                self.selection.setHeight(h)
                self.updateMask()
        self.update()

    def paintEvent(self, evt):
        # draw background
        rect = self.rect()
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(rect, self.screen)
        painter.drawPixmap(rect, self.mask)

        if self.selection != None:
            painter.setPen(_borderPen)
            painter.setBrush(_borderBrush)
            painter.setFont(_labelFont)
            drawRect = lambda center: painter.drawRect(center.x()-2, center.y()-2, 4, 4)
            p0 = self.selection.topLeft()
            p1 = self.selection.bottomLeft()
            p2 = self.selection.bottomRight()
            p3 = self.selection.topRight()
            x, y = self.selection.x(), self.selection.y()
            w, h = self.selection.width(), self.selection.height()
            if w == 0 and h == 0:
                drawRect(p0)
            elif w == 0:
                painter.drawLine(p0, p1)
                drawRect(p0)
                drawRect(p1)
                drawRect((p0 + p1) / 2)
            elif h == 0:
                painter.drawLine(p1, p2)
                drawRect(p1)
                drawRect(p2)
                drawRect((p1 + p2) / 2)
            else:
                painter.drawLine(p0, p1)
                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
                painter.drawLine(p3, p0)
                drawRect(p0)
                drawRect(p1)
                drawRect(p2)
                drawRect(p3)
                drawRect((p0 + p1) / 2)
                drawRect((p1 + p2) / 2)
                drawRect((p2 + p3) / 2)
                drawRect((p3 + p0) / 2)
            if y < 16:
                painter.setPen(Qt.black)
                painter.drawText(x + 2, y + 12, f'{w} x {h}')
            else:
                painter.setPen(Qt.white)
                painter.drawText(x, y - 5, f'{w} x {h}')

        if self.state == self.Selected: return
        if self.reselectable == 'move': return
        # draw cursor info
        pos = QCursor.pos()
        px, py = pos.x(), pos.y()
        offset, size, halfSize = 20, 110, 55
        x, y = px + offset, py + offset
        w, h = rect.width(), rect.height()
        if x + size > w: x = px - offset - size
        if y + size > h - 45: y = py - offset - size - 35
        painter.setPen(_borderPen)
        painter.drawPixmap(x, y, size, size, self.screen, px - 10, py - 10, 20, 20)
        painter.drawLine(x, y, x + size, y)
        painter.drawLine(x + size, y, x + size, y + size)
        painter.drawLine(x + size, y + size, x, y + size)
        painter.drawLine(x, y + size, x, y)
        painter.drawLine(x + halfSize, y, x + halfSize, y + size)
        painter.drawLine(x, y + halfSize, x + size, y + halfSize)

        painter.setPen(Qt.white)
        painter.setFont(_labelFont)
        painter.fillRect(x - 1, y + size, size + 2, 32, self.maskClearColor)
        painter.drawText(x + 5, y + size + 13, f'POS: {px} {py}')
        color = self.screenImg.pixelColor(px, py)
        painter.drawText(x + 5, y + size + 26, f'RGB: {color.red()} {color.green()} {color.blue()}')

    def closeEvent(self, evt):
        super().closeEvent(evt)
        self.clearOverrideCursor()
        Screenshot.Instance = None

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Screenshot()
    w.show()
    sys.exit(app.exec_())
