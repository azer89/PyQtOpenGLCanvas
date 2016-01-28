
"""
Some examples:

http://stackoverflow.com/questions/21574723/save-image-from-opengl-pyqt-in-high-resolution
"""

import numpy

from OpenGL.GL import *
from PyQt4 import QtOpenGL
from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *

class MyBufferPainter(object):

    def __init__(self):
        print "MyBufferPainter"

    def initializeGL(self):
        # texture
        self.__ori_tex = self.bindTexture(QtGui.QPixmap("laughing_man.png"))

        self.__shaderProgram.link()

        self.__texCoordLocation   = self.__shaderProgram.attributeLocation("uv")
        self.__vertexLocation     = self.__shaderProgram.attributeLocation("position")
        self.__colorLocation      = self.__shaderProgram.attributeLocation("color")
        self.__use_color_location = self.__shaderProgram.uniformLocation("use_color")
        self.__mvpMatrixLocation  = self.__shaderProgram.uniformLocation("mvpMatrix")

        vertexData = numpy.array([   0.0,   0.0, 0.0, 1.0,
                                     0.0, 250.0, 0.0, 1.0,
                                   250.0, 250.0, 0.0, 1.0,

                                     0.0,   0.0, 0.0, 1.0,
                                   250.0, 250.0, 0.0, 1.0,
                                   250.0,   0.0, 0.0, 1.0,

                                # uv
                                0, 1,
                                0, 0,
                                1, 0,

                                0, 1,
                                1, 0,
                                1, 1],
                                dtype = numpy.float32)

        colorData = numpy.array([1.0, 0.0, 0.0, 1.0,
                                 0.0, 0.0, 1.0, 1.0,
                                 0.0, 1.0, 0.0, 1.0,
                                 1.0, 0.0, 0.0, 1.0,
                                 0.0, 1.0, 0.0, 1.0,
                                 0.0, 0.0, 1.0, 1.0,],
                                 dtype = numpy.float32)

        # create VAO
        self.__VAO = glGenVertexArrays(1)
        glBindVertexArray(self.__VAO)

        # create a VBO for position and uv
        posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation)
        glVertexAttribPointer(self.__vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self.__texCoordLocation)
        glVertexAttribPointer(self.__texCoordLocation, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(96))

        # create VBO for color
        colVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colVBO)
        glBufferData(GL_ARRAY_BUFFER, colorData.nbytes, colorData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__colorLocation)
        glVertexAttribPointer(self.__colorLocation,    4, GL_FLOAT, GL_FALSE, 0, None)

        # unbind vao and vbo
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        #pass

    def paintGL(self):
        pass
