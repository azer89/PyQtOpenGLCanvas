
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

class GLContainer(QWidget):
    """
    Class GLContainer
    """
    def __init__(self):
        super(GLContainer, self).__init__()

        self.glWidget = GLWidget()

        mainLayout = QtGui.QHBoxLayout()

        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)

        self.setWindowTitle("Hello GL")

        QtCore.QCoreApplication.instance().aboutToQuit.connect( self.DeleteGLWidget )

    def DeleteGLWidget(self):
        print "QUIT"
        self.glWidget.setParent(None)
        del self.glWidget
        