
"""
https://github.com/Werkov/PyQt4/blob/master/examples/opengl/hellogl.py
https://github.com/prideout/coregl-python
http://stackoverflow.com/questions/11192938/compiling-shaders-in-pyqt

"""

import sys

from PyQt4 import QtCore, QtGui

from GLContainer import GLContainer
    
    
if __name__ == '__main__':
    app_created = False

    app = QtCore.QCoreApplication.instance()
    
    if app is None:
        app = QtGui.QApplication(sys.argv)
        app_created = True
    
    app.references = set()
    
    window = GLContainer()    
    window.resize(1024, 768)
    app.references.add(window)
    window.show()
    
    if app_created:
        app.exec_()

    # issue:
    # http://stackoverflow.com/questions/15861839/error-upon-app-shutdown-qglcontextmakecurrent-cannot-make-invalid-context-cu
    #app.instance().aboutToQuit.connect( window.DeleteGLWidget() )