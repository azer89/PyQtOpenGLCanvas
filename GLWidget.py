
"""
GLWidget
"""

import sys
#import pdb

from PyQt4 import QtCore, QtGui, QtOpenGL
#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader, QGLFormat, QGLContext, QGLWidget
from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
#from PyQt4.QtGui import QMatrix4x4 #, QOpenGLBuffer, QOpenGLVertexArrayObject


from Utility import *

"""
Importing OpenGL
"""
try:
    from OpenGL import GL
except ImportError:
    print "You need to install PyOpenGL"
    sys.exit(1)
else:
    print "OpenGL OK"

class GLWidget(QtOpenGL.QGLWidget):
    """
    Class GLWidget
    """
    
    def __init__(self, parent = None):
        if hasattr(QGLFormat, 'setVersion'):
            # Modern OpenGL
            f = QGLFormat()
            f.setVersion(3, 3)
            f.setProfile(QGLFormat.CoreProfile)
            c = QGLContext(f, None)
            QGLWidget.__init__(self, c, parent)
            print "Version is set to 3.3"
        else:
            QGLWidget.__init__(self, parent)
        
        self.backColor = QtGui.QColor.fromRgbF(1.0, 1.0, 1.0, 1.0)

        
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
    
    def sizeHint(self):
        return QtCore.QSize(1024, 768)
    
    def initializeGL(self):
        
        # shaders
        self._shaderProgram = QGLShaderProgram()
        if self._shaderProgram.addShaderFromSourceFile(QGLShader.Vertex, "shader.vert") :
            print "Vertex shader OK"
        if self._shaderProgram.addShaderFromSourceFile(QGLShader.Fragment, "shader.frag") :
            print "Fragment shader OK"
        print self._shaderProgram.log()
        self._shaderProgram.bind() # or link()
        
        self._mvpMatrixLocation  = self._shaderProgram.uniformLocation("mvpMatrix")
        self._colorLocation      = self._shaderProgram.attributeLocation("vertexColor")
        self._vertexLocation     = self._shaderProgram.attributeLocation("vert")
        self._use_color_location = self._shaderProgram.uniformLocation("use_color")
                
        
        self.qglClearColor(self.backColor)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_DEPTH_TEST)

        #print self.width()
        #print self.height()

        """
        // points
        QOpenGLBuffer            _pointsVbo;
        QOpenGLVertexArrayObject _pointsVao;

        // lines
        QOpenGLBuffer            _linesVbo;
        QOpenGLVertexArrayObject _linesVao;
        """

    def createPoints(self):

        # generate points
        self._points = []

        centerX = self.width() / 2.0
        centerY = self.height() / 2.0
        radius = 5.0
        n_slice = 8
        add_value = np.pi * 2.0 / n_slice
        thetas = np.arange(0.0, np.pi * 2.0, add_value)
        points = []
        for t in thetas:
            xPt = centerX + radius * np.sin(t)
            yPt = centerY + radius * np.cos(t)
            points.append(np.array([xPt, yPt]))

        self._pointsVao = GL.glGenVertexArrays(1)
        self._pointsVbo = GL.glGenBuffers(1)

        # bind VAO
        GL.glBindVertexArray(self._pointsVao)

    
    def paintGL(self):
        print "paint"
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        GL.glViewport(0, 0, self.width(),  self.height())  
        
        #pdb.set_trace()
        #orthoMatrix = QMatrix4x4()

        #orthoMatrix = QMatrix4x4().ortho(0.0, self.width(), self.height(), 0, -100, 100)
        #transformMatrix = QMatrix4x4().setToIdentity()

        orthoMatrix = QMatrix4x4()
        orthoMatrix.ortho(0.0, self.width(), self.height(), 0, -100, 100)

        transformMatrix = QMatrix4x4()
        transformMatrix.setToIdentity()

        mpvMatrix = orthoMatrix * transformMatrix
        self._shaderProgram.setUniformValue(self._mvpMatrixLocation, mpvMatrix)

        #print mpvMatrix
        
        #print orthoMatrix
        #print transformMatrix        
        #GL.glLoadIdentity()
        
    def updateGL(self):
        pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        