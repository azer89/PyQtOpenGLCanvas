
"""
GLContainer
"""

import sys
import numpy
from OpenGL.GL import *

from PyQt4.QtGui import QWidget
from PyQt4 import QtGui, QtCore

from PyQt4 import QtGui, QtOpenGL

from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader
#from PyQt4.QtGui import QMatrix4x4

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
        self.verticalScrollBar().setSingleStep(10)
        self.verticalScrollBar().setPageStep(100)
        self.horizontalScrollBar().setVisible(True)
        self.verticalScrollBar().setVisible(True)

        self._glWidget = GLWidget()

        self.setViewport(self._glWidget)

        self.setMouseTracking(True)

        #mainLayout = QtGui.QHBoxLayout()
        #mainLayout.addWidget(self._glWidget)
        #self.setLayout(mainLayout)
        #self.setWindowTitle("Hello GL")

        QtCore.QCoreApplication.instance().aboutToQuit.connect( self.DeleteGLWidget )

    def DeleteGLWidget(self):
        print "QUIT"
        self._glWidget.setParent(None)
        del self._glWidget

    def paintEvent(self, QPaintEvent):


        self._glWidget.updateGL()

    #def paintEvent(self):
    #    pass
        