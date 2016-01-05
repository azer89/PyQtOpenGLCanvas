
"""
GLContainer
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget

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

        