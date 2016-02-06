
"""
Some examples:

http://stackoverflow.com/questions/21574723/save-image-from-opengl-pyqt-in-high-resolution
"""


import numpy

from OpenGL.GL import *
from PyQt4 import QtOpenGL
from PyQt4.QtOpenGL import *
from PyQt4 import QtGui
from PyQt4.QtGui import *

from PyQt4.QtOpenGL import QGLFramebufferObject

class MyBufferPainter(object):

    #def __init__(self, parent = None):
    def __init__(self):
        #QGLWidget.__init__(self, parent)
        print "MyBufferPainter"

    def SetThings(self, shaderProgram, texCoordLocation, vertexLocation, colorLocation, use_color_location, mvpMatrixLocation):
        self.__shaderProgram = shaderProgram

        self.__texCoordLocation   = texCoordLocation
        self.__vertexLocation     = vertexLocation
        self.__colorLocation      = colorLocation
        self.__use_color_location = use_color_location
        self.__mvpMatrixLocation  = mvpMatrixLocation

    # INITIALIZE BUFFER !!!
    def initializeGL(self, ori_tex):
        # texture
        self.__ori_tex = ori_tex

        """
        vertexData = numpy.array([-10.0, -10.0, 0.0, 1.0,  # top left
                                  -20.0, 250.0, 0.0, 1.0,  # bottom left
                                  290.0, 290.0, 0.0, 1.0,  # bottom right

                                  -10.0, -10.0, 0.0, 1.0,  # top left
                                  290.0, 290.0, 0.0, 1.0,  # bottom right
                                  250.0,   0.0, 0.0, 1.0,  # top right

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
        """


        """
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
        """

        # unbind vao and vbo
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindVertexArray(0)
        #pass

    def prepareFrameRect(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):
        """
        xLeft  = 0 + x_offset
        xRight = frame_width + x_offset

        yTop    = 0 + y_offset
        yBottom = frame_height + y_offset

        invScale = 1.0 / zoom_factor

        xLeft   *= invScale
        xRight  *= invScale
        yTop    *= invScale
        yBottom *= invScale

        vertexData = numpy.array([xLeft,  yTop,    0.0, 1.0,  # top left
                                  xLeft,  yBottom, 0.0, 1.0,    # bottom left
                                  xRight, yBottom, 0.0, 1.0,      # bottom right

                                  xLeft,  yTop,    0.0, 1.0, # top left
                                  xRight, yBottom, 0.0, 1.0,     # bottom right
                                  xRight, yTop,    0.0, 1.0,     # top right

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
        self.__bufferVAO = glGenVertexArrays(1)
        glBindVertexArray(self.__bufferVAO)

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
        """


    def paintFullScreen(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):
        """
        see this:
        https://raw.githubusercontent.com/azer89/ComicsVectorizer/master/CVUserInterface/RenderUtility.cpp
        void RenderUtility::DrawFullscreen
        """
        #self.prepareFrameRect(x_offset, y_offset, frame_width, frame_height, zoom_factor)

        #frameBufferA = QGLFramebufferObject(frame_width, frame_height)
        #frameBufferA.bind()

        """
        self.__shaderProgram.setUniformValue(self.__use_color_location, 1.0)
        # bind VAO
        glBindVertexArray(self.__bufferVAO)
        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 18)
        """

        #frameBufferA.release()



    # DRAW BUFFER !!!
    def paintGL(self):
        """
        # DRAW SOMETHING
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        # bind texture
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        # bind VAO
        glBindVertexArray(self.__VAO)
        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 18)
        """


