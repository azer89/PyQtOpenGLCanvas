
from PyQt4.QtCore import QSize, QRect

from PyQt4 import QtSvg
from PyQt4.QtCore import Qt
from PyQt4.QtGui import *

class MySvgWriter(object):
    #condition = 'New'

    def __init__(self):
        print "MySvgWriter"

    def DrawSomething(self):
        print "MySvgWriter.DrawSomething"

        gen = QtSvg.QSvgGenerator()
        gen.setFileName("output.svg")
        gen.setSize(QSize(200, 200))
        gen.setViewBox(QRect(0, 0, 200, 200))
        #gen.setDescription(self.tr("YOLO" "YOYO"))

        painter = QPainter()
        painter.begin(gen)

        painter.setClipRect(QRect(0, 0, 200, 200))
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 200, 200), Qt.darkBlue)

        painter.end()

    #def drive(self):
    #    self.condition = 'Used'