
"""
GLContainer


radhitya@uwaterloo.ca
"""

import sys
import numpy as np
from OpenGL.GL import *

from PyQt4.QtGui import QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSize, QPoint

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4 import QtGui, QtOpenGL

from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader
#from PyQt4.QtGui import QMatrix4x4
from numpy.core.fromnumeric import put

from GLWidget import GLWidget
from GLWidget import QAbstractScrollArea, QPaintEvent


class GLContainer(QAbstractScrollArea):
    """
    Class GLContainer
    """
    def __init__(self):
        super(GLContainer, self).__init__()

        self.horizontalScrollBar().setSingleStep(10)
        self.horizontalScrollBar().setPageStep(100)
        self.horizontalScrollBar().setVisible(True)

        self.verticalScrollBar().setSingleStep(10)
        self.verticalScrollBar().setPageStep(100)
        self.verticalScrollBar().setVisible(True)

        self.horizontalScrollBar().valueChanged.connect(self.HScrollChanged)
        self.verticalScrollBar().valueChanged.connect(self.VScrollChanged)

        self.__glWidget = GLWidget()
        self.setViewport(self.__glWidget)

        self.setMouseTracking(True)


        self.__mousePressed = False
        self.__ctrlPressed = False
        self.__scrollMoved = False
        self.__xPrevF = 0.0
        self.__yPrevF = 0.0
        self.__prevZoomFactor = self.__glWidget.GetZoomFactor()
        self.__mousePos = QPointF(0, 0)

        QtCore.QCoreApplication.instance().aboutToQuit.connect( self.DeleteGLWidget )

        self.__justInitialized = True

        self.UpdateViewport(True)


    def HScrollChanged(self, val):
        self.__xPrevF = float(val)
        self.__glWidget.SetHorizontalScroll(val)
        self.__scrollMoved = True


    def VScrollChanged(self, val):
        self.__yPrevF = float(val)
        self.__glWidget.SetVerticalScroll(val)
        self.__scrollMoved = True


    def UpdateViewport(self, putInMiddle = False):

        """
        leftRange  = 0
        rightRange = 0
        upRange    = 0
        downRange  = 0

        hPos = 0
        vPos = 0
        """

        barSize = QSize(self.width() - 20, self.height() - 20)
        zoomFactor = self.__glWidget.GetZoomFactor()

        imgSize = self.__glWidget.GetImageSize()

        img_width = float(imgSize.width() * zoomFactor)
        img_height = float(imgSize.height() * zoomFactor)

        if (img_width == 0 or img_height == 0):
            print "duh"
            img_width = 100 * zoomFactor
            img_height  = 100 * zoomFactor

        xSPos = 0
        ySPos = 0

        if not putInMiddle:
            xNormPos = float(self.__mousePos.x()) + self.__xPrevF
            yNormPos = float(self.__mousePos.y()) + self.__yPrevF
            xNormPos /= self.__prevZoomFactor
            yNormPos /= self.__prevZoomFactor

            xRev = float(xNormPos) * zoomFactor
            yRev = float(yNormPos) * zoomFactor
            xSPos = xRev - float(self.__mousePos.x())
            ySPos = yRev - float(self.__mousePos.y())

        xGap = np.abs(barSize.width() - img_width)
        yGap = np.abs(barSize.height() - img_height)

        if(img_width <= barSize.width()) :
            if(putInMiddle):
                hPos = -xGap * 0.5
            else:
                hPos  = xSPos

            leftRange  = -img_width - xGap
            rightRange = img_width
        else :
            if(putInMiddle):
                hPos = xGap * 0.5
            else:
                hPos  = xSPos

            leftRange  = -img_width + xGap
            rightRange = img_width

        if(img_height <= barSize.height()) :
            if(putInMiddle):
                vPos = -yGap * 0.5
            else:
                vPos = ySPos

            upRange   = -img_height - yGap
            downRange = img_height
        else :
            if(putInMiddle):
                vPos = yGap * 0.5
            else:
                vPos = ySPos

            upRange   = -img_height + yGap
            downRange = img_height


        self.__xPrevF = hPos
        self.__yPrevF = vPos

        self.horizontalScrollBar().setRange(leftRange, rightRange)
        self.verticalScrollBar().setRange(upRange, downRange)

        self.horizontalScrollBar().setSliderPosition(hPos)
        self.verticalScrollBar().setSliderPosition(vPos)

    def setScrolls(self):
        """
        Currently not being used...
        """
        self.horizontalScrollBar().setVisible(True)
        self.verticalScrollBar().setVisible(True)

        self.__prevZoomFactor = 1.0

        # nasty code here...
        shouldZoom = True
        while(shouldZoom):
            w = self.width()
            h = self.height()
            imgSize = self.__glWidget.GetImageSize()
            if(imgSize.width() == 0 or imgSize.height() == 0):
                imgSize = QSize(100, 100)

            zoomFactor = self.__glWidget.GetZoomFactor()

            if( w < imgSize.width() * zoomFactor or h < imgSize.height() *zoomFactor):
                self.__glWidget.ZoomOut()
            else:
                shouldZoom = False

        self.UpdateViewport(True)


    def mousePressEvent(self, event):
        super(GLContainer, self).mousePressEvent(event)
        #pass


    def mouseMoveEvent(self, event):
        super(GLContainer, self).mouseMoveEvent(event)
        self.__mousePos.setX( event.x() )
        self.__mousePos.setY( event.y() )



    def mouseReleaseEvent(self, event):
        #pass
        super(GLContainer, self).mouseReleaseEvent(event)


    def wheelEvent(self, event):
        #super(GLContainer, self).wheelEvent(event) # don't uncomment !!!
        scrollDir = True if (event.delta() > 0) else False
        self.__prevZoomFactor = self.__glWidget.GetZoomFactor()

        if (scrollDir):
            self.__glWidget.ZoomOut()
        else :
            self.__glWidget.ZoomIn()

        # update scrollbars
        self.UpdateViewport()



    def keyPressEvent(self, event):
        super(GLContainer, self).keyPressEvent(event)

        if (event.key() == Qt.Key_Control):
            #print "CRTL pressed"
            self.__ctrlPressed = True
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

        #if (event.key() == Qt.Key_Right)
        #    self.__glWidget.AddSlice()
        #elif (event.key() == Qt.Key_Left):
        #    self.__glWidget.RemoveSlice()

        self.__glWidget.updateGL()


    def keyReleaseEvent(self, event):
        super(GLContainer, self).keyReleaseEvent(event)

        if (event.key() == Qt.Key_Control):
            #print "CRTL released"
            self.__ctrlPressed = False
            QApplication.restoreOverrideCursor()


    def DeleteGLWidget(self):
        print "QUIT"
        self.__glWidget.setParent(None)
        del self.__glWidget


    def paintEvent(self, event):

        if(self.__justInitialized):
            self.UpdateViewport(True)
            self.__justInitialized = False

        self.__glWidget.updateGL()