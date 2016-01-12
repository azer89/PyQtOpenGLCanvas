import sys
import numpy
from OpenGL.GL import *

from PyQt4.QtGui import QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSize

from PyQt4 import QtGui, QtOpenGL

from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader
#from PyQt4.QtGui import QMatrix4x4


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent = None):

        self.__image_width  = 50
        self.__image_height = 50

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


    def GetImageSize(self):
        return QSize(self.__image_width, self.__image_height)


    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glViewport(0, 0, self.width(), self.height())

        self.__shaderProgram = QGLShaderProgram()

        if self.__shaderProgram.addShaderFromSourceFile(QGLShader.Vertex, "shader.vert") :
            print "Vertex shader OK"

        if self.__shaderProgram.addShaderFromSourceFile(QGLShader.Fragment, "shader.frag") :
            print "Fragment shader OK"

        # texture
        self.__ori_tex = self.bindTexture(QtGui.QPixmap("laughing_man.png"))

        self.__shaderProgram.link()

        self.__texCoordLocation   = self.__shaderProgram.attributeLocation("uv")
        self.__vertexLocation     = self.__shaderProgram.attributeLocation("position")
        self.__colorLocation      = self.__shaderProgram.attributeLocation("color")

        self.__use_color_location = self.__shaderProgram.uniformLocation("use_color")
        self.__mvpMatrixLocation  = self.__shaderProgram.uniformLocation("mvpMatrix")

                                # position
        vertexData = numpy.array([250.0,  20.0, 0.0, 1.0,
                                  100.0, 300.0, 0.0, 1.0,
                                  560.0, 400.0, 0.0, 1.0,

                                # uv
                                0.0, 1.0,
                                0.0, 0.0,
                                1.0, 0.0],
                                dtype = numpy.float32)

        colorData = numpy.array([1.0, 0.0, 0.0, 1.0,
                                 0.0, 0.0, 1.0, 1.0,
                                 0.0, 1.0, 0.0, 1.0],
                                 dtype = numpy.float32)

        # create VAO
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # create a VBO for position and uv
        posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation)
        glVertexAttribPointer(self.__vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self.__texCoordLocation)
        glVertexAttribPointer(self.__texCoordLocation, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(48))

        # create VBO for color
        colVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colVBO)
        glBufferData(GL_ARRAY_BUFFER, colorData.nbytes, colorData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__colorLocation)
        glVertexAttribPointer(self.__colorLocation,    4, GL_FLOAT, GL_FALSE, 0, None)

        # unbind vao and vbo
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def paintGL(self):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        orthoMatrix = QMatrix4x4()
        orthoMatrix.ortho(0.0, self.width() , self.height(), 0, -100, 100)
        transformMatrix = QMatrix4x4()
        transformMatrix.setToIdentity()
        mpvMatrix = orthoMatrix * transformMatrix

        # activate shader program
        self.__shaderProgram.bind()
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        glBindTexture(GL_TEXTURE_2D, self._ori_tex)
        self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)

        glBindVertexArray(self.VAO)

        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 9)

        glBindVertexArray(0)
        glUseProgram(0)