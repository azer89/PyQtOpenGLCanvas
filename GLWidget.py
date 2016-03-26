
"""
Reza Adhitya Saputra
reza.adhitya.saputra@gmail.com
"""

import sys
import numpy

from OpenGL.GL import *
from PyQt4 import QtOpenGL
from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *

from PyQt4 import QtGui
from PyQt4.QtCore import QSize, QPoint
from PyQt4.QtGui import QWidget
from PyQt4 import QtCore
from PyQt4 import QtSvg

from OpenGL.GL.framebufferobjects import *

from MySvgTool import MySvgTool
from MySvgWriter import MySvgWriter
from MyBufferPainter import MyBufferPainter

#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader
#from PyQt4.QtGui import QMatrix4x4


class GLWidget(QtOpenGL.QGLWidget):
    """
    This class renders something with OpenGL
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        self.__image_width  = 250
        self.__image_height = 250

        self.__isMouseDown = False
        self.__zoomFactor = 1.0

        self.__scrollOffset = QPoint()

        if hasattr(QGLFormat, "setVersion"):
            # Modern OpenGL
            f = QGLFormat()
            f.setVersion(3, 3)
            f.setProfile(QGLFormat.CoreProfile)
            f.setSampleBuffers(True)
            c = QGLContext(f, None)

            QGLWidget.__init__(self, c, parent)
            print "Version is set to 3.3"
        else:
            QGLWidget.__init__(self, parent)

        #self.__svgItem = QtSvg.QGraphicsSvgItem("circle_star.svg")
        self.__mySvgTool = MySvgTool()

        self.__mySvgWriter = MySvgWriter()
        self.__mySvgWriter.DrawSomething()
        self.__myBufferPainter = MyBufferPainter()


    def initializeGL(self):

        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        self.__shaderProgram = QGLShaderProgram()
        if self.__shaderProgram.addShaderFromSourceFile(QGLShader.Vertex, "shader.vert") :
            print "Main - Vertex shader OK"
        if self.__shaderProgram.addShaderFromSourceFile(QGLShader.Fragment, "shader.frag") :
            print "Main - Fragment shader OK"
        self.__shaderProgram.link()

        self.__texCoordLocation   = self.__shaderProgram.attributeLocation("uv")
        self.__vertexLocation     = self.__shaderProgram.attributeLocation("position")
        self.__colorLocation      = self.__shaderProgram.attributeLocation("color")
        self.__use_color_location = self.__shaderProgram.uniformLocation("use_color")
        self.__mvpMatrixLocation  = self.__shaderProgram.uniformLocation("mvpMatrix")

        # Returns -1 if name is not a valid attribute for this shader program.
        print "\n__texCoordLocation   :", self.__texCoordLocation, " ",   \
              "\n__vertexLocation     :", self.__vertexLocation, " ",     \
              "\n__colorLocation      :", self.__colorLocation, " ",      \
              "\n__use_color_location :", self.__use_color_location, " ", \
              "\n__mvpMatrixLocation  :", self.__mvpMatrixLocation


        self.__blurProgram = QGLShaderProgram()
        if self.__blurProgram.addShaderFromSourceFile(QGLShader.Vertex, "shader.vert") :
            print "Gaussian blur - Vertex shader OK"

        # if I use shader.frag it's okay ???
        # if self.__blurProgram.addShaderFromSourceFile(QGLShader.Fragment, "gaussian_blur.frag") :
        if self.__blurProgram.addShaderFromSourceFile(QGLShader.Fragment, "gaussian_blur.frag") :
            print "Gaussian blur - fragment shader OK"
        self.__blurProgram.link()

        self.__myBufferPainter.SetThings(self.__shaderProgram, self.__blurProgram)
        self.__myBufferPainter.initializeGL(self.bindTexture(QtGui.QPixmap("laughing_man.png")))
        self.__myBufferPainter.prepareFrameRect(self.__scrollOffset.x(),  self.__scrollOffset.y(), self.width(), self.height(), self.__zoomFactor)

        """
        ### texture
        self.__ori_tex = self.bindTexture(QtGui.QPixmap("laughing_man.png"))

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

        ### create VAO
        self.__VAO = glGenVertexArrays(1)
        glBindVertexArray(self.__VAO)

        ### create a VBO for position and uv
        posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation)
        glVertexAttribPointer(self.__vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self.__texCoordLocation)
        glVertexAttribPointer(self.__texCoordLocation, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(96))

        ### create VBO for color
        colVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colVBO)
        glBufferData(GL_ARRAY_BUFFER, colorData.nbytes, colorData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__colorLocation)
        glVertexAttribPointer(self.__colorLocation,    4, GL_FLOAT, GL_FALSE, 0, None)

        ### unbind vao and vbo
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        """


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ### this doesn't work
        #frameBufferA.bind()
        #frameBufferA.release()

        glViewport(0, 0, self.width() , self.height())

        orthoMatrix = QMatrix4x4()
        orthoMatrix.ortho(0 +  self.__scrollOffset.x(),
                          self.width() +  self.__scrollOffset.x(),
                          self.height() +  self.__scrollOffset.y(),
                          0 +  self.__scrollOffset.y(),
                          -100, 100)
        transformMatrix = QMatrix4x4()
        transformMatrix.setToIdentity()
        transformMatrix.scale(self.__zoomFactor)

        ### activate shader program
        #self.__shaderProgram.bind()
        ### set a shader attribute (0 means use texture, 1 means use color)
        #self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)

        ### feed the mpv matrix
        mpvMatrix = orthoMatrix * transformMatrix
        #self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)

        # Draw Something
        self.__myBufferPainter.paintGL(self.__scrollOffset.x(),  self.__scrollOffset.y(), self.width(), self.height(), self.__zoomFactor, mpvMatrix)

        """
        ### DRAW SOMETHING
        ### bind texture
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        ### bind VAO
        glBindVertexArray(self.__VAO)
        ### draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 18)
        """

        ### unbind
        #glBindVertexArray(0)
        #glUseProgram(0)
        #self.__shaderProgram.release()

    def SetSomething(self):
        pass

    def DrawSomething(self):
        pass


    def ZoomIn(self):
        self.__zoomFactor += 0.1


    def ZoomOut(self):
        self.__zoomFactor -= 0.1
        if(self.__zoomFactor < 0.1):
            self.__zoomFactor = 0.1

    """
    Get / Set
    """
    def GetImageSize(self):
        """
        Get the size of the canvas / image
        """
        return QSize(self.__image_width, self.__image_height)


    def SetZoomFactor(self, val):
        """
        Set the value of magnification
        """
        self.__zoomFactor = val


    def GetZoomFactor(self):
        """
        Obtain the value of the magnification
        """
        return self.__zoomFactor


    def SetMouseDown(self, val):
        """
        Set the value of mouse down
        """
        self.__isMouseDown = val

    def SetHorizontalScroll(self, val):
        """
        Set horizontal scroll value
        """
        self.__scrollOffset.setX(val)


    def SetVerticalScroll(self, val):
        """
        Set vertical scroll value
        """
        self.__scrollOffset.setY(val)