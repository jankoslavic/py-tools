#!/usr/bin/python
# -*- coding: utf8 -*-
#  see: http://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget
# by: Jean-Sébastien

import sys
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PySide import QtGui, QtCore

def mathTex_to_QPixmap(mathTex, fs):

    #---- set up a mpl figure instance ----

    fig = mpl.figure.Figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    #---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    t = ax.text(0, 0, mathTex, ha='left', va='bottom', fontsize=fs)

    #---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth, tight_fheight)

    #---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1],
                                                  QtGui.QImage.Format_ARGB32))
    qpixmap = QtGui.QPixmap(qimage)

    return qpixmap


class MyQTableWidget(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)

        self.setHorizontalHeader(MyHorizHeader(self))

    def setHorizontalHeaderLabels(self, headerLabels, fontsize):

        qpixmaps = []
        for indx, labels in enumerate(headerLabels):
            qpixmaps.append(mathTex_to_QPixmap(labels, fontsize))
            self.setColumnWidth(indx, qpixmaps[indx].size().width() + 16)

        self.horizontalHeader().qpixmaps = qpixmaps

        super(MyQTableWidget, self).setHorizontalHeaderLabels(headerLabels)


class MyHorizHeader(QtGui.QHeaderView):
    def __init__(self, parent):
        super(MyHorizHeader, self).__init__(QtCore.Qt.Horizontal, parent)

        self.setClickable(True)
        self.setStretchLastSection(True)

        self.qpixmaps = []

    def paintSection(self, painter, rect, logicalIndex):

        if not rect.isValid():
            return

        #------------------------------ paint section (without the label) ----

        opt = QtGui.QStyleOptionHeader()
        self.initStyleOption(opt)

        opt.rect = rect
        opt.section = logicalIndex
        opt.text = ""

        #---- mouse over highlight ----

        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        if rect.contains(mouse_pos):
            opt.state |= QtGui.QStyle.State_MouseOver

        #---- paint ----

        painter.save()
        self.style().drawControl(QtGui.QStyle.CE_Header, opt, painter, self)
        painter.restore()

        #------------------------------------------- paint mathText label ----

        qpixmap = self.qpixmaps[logicalIndex]

        #---- centering ----

        xpix = (rect.width() - qpixmap.size().width()) / 2. + rect.x()
        ypix = (rect.height() - qpixmap.size().height()) / 2.

        #---- paint ----

        rect = QtCore.QRect(xpix, ypix, qpixmap.size().width(),
                            qpixmap.size().height())
        painter.drawPixmap(rect, qpixmap)

    def sizeHint(self):

        baseSize = QtGui.QHeaderView.sizeHint(self)

        baseHeight = baseSize.height()
        if len(self.qpixmaps):
            for pixmap in self.qpixmaps:
               baseHeight = max(pixmap.height() + 8, baseHeight)
        baseSize.setHeight(baseHeight)

        self.parentWidget().repaint()

        return baseSize


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    w = MyQTableWidget()
    w.verticalHeader().hide()

    headerLabels = [
        '$C_{soil}=(1 - n) C_m + \\theta_w C_w$',
        '$k_{soil}=\\frac{\\sum f_j k_j \\theta_j}{\\sum f_j \\theta_j}$',
        '$\\lambda_{soil}=k_{soil} / C_{soil}$',
        '$H_1$ [g/N]']

    w.setColumnCount(len(headerLabels))
    w.setHorizontalHeaderLabels(headerLabels, 18)
    w.setRowCount(3)
    w.setAlternatingRowColors(True)

    k = 1
    for j,_ in enumerate(headerLabels):
        for i in range(3):
            w.setItem(i, j, QtGui.QTableWidgetItem('Value %i' % (k)))
            k += 1

    w.show() 
    w.resize(800, 200)

    sys.exit(app.exec_())