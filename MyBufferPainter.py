
import numpy

from OpenGL.GL import *
from PyQt4 import QtOpenGL
from PyQt4.QtOpenGL import *
from PyQt4 import QtGui
from PyQt4.QtGui import *

#from PyQt4.QtOpenGL import QGLFramebufferObject # doesn't work
from OpenGL.GL.framebufferobjects import *

"""
see this:
https://raw.githubusercontent.com/azer89/ComicsVectorizer/master/CVUserInterface/RenderUtility.cpp
void RenderUtility::DrawFullscreen

# FrameBufferObject documentation
http://pyqt.sourceforge.net/Docs/PyQt4/qglframebufferobject.html#QGLFramebufferObject
"""

### ???
# http://stackoverflow.com/questions/8016050/pyqt-with-interactive-svg-images

### render svg using frame buffer
# https://github.com/RSATom/Qt/tree/master/qtsvg/examples/svg/opengl

### parse with something and render using qt
# http://stackoverflow.com/questions/1359003/svg-example-in-c-c

### examples of frame buffers
# http://stackoverflow.com/questions/21574723/save-image-from-opengl-pyqt-in-high-resolution

### this is an example of rendering svg but doesn't use frame buffer
# http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/painting/svgviewer/svgviewer.py

### pyqt4 examples, still using the old opengl:
# https://github.com/Werkov/PyQt4/tree/master/examples

class MyBufferPainter(object):

    def __init__(self):
        print "MyBufferPainter"

    def SetThings(self, shaderProgram, texCoordLocation, vertexLocation, colorLocation, use_color_location, mvpMatrixLocation):
        self.__shaderProgram = shaderProgram

        self.__texCoordLocation   = texCoordLocation
        self.__vertexLocation     = vertexLocation
        self.__colorLocation      = colorLocation
        self.__use_color_location = use_color_location
        self.__mvpMatrixLocation  = mvpMatrixLocation

    def initializeGL(self, ori_tex):
        ### texture
        self.__ori_tex = ori_tex

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


        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def prepareFrameRect(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):
        xLeft  = 0 + x_offset + 100
        xRight = frame_width + x_offset - 100

        yTop    = 0 + y_offset + 100
        yBottom = frame_height + y_offset -100

        invScale = 1.0 / zoom_factor

        xLeft   *= invScale
        xRight  *= invScale
        yTop    *= invScale
        yBottom *= invScale

        vertexData = numpy.array([xLeft,  yTop,    -5.0, 1.0,  # top left
                                  xLeft,  yBottom, -5.0, 1.0,  # bottom left
                                  xRight, yBottom, -5.0, 1.0,  # bottom right
                                  xLeft,  yTop,    -5.0, 1.0,  # top left
                                  xRight, yBottom, -5.0, 1.0,  # bottom right
                                  xRight, yTop,    -5.0, 1.0,   # top right
                                  ],
                                  dtype = numpy.float32)

        colorData = numpy.array([1.0, 0.0, 0.0, 1.0,
                                 0.0, 0.0, 1.0, 1.0,
                                 0.0, 1.0, 0.0, 1.0,
                                 1.0, 0.0, 0.0, 1.0,
                                 0.0, 1.0, 0.0, 1.0,
                                 0.0, 0.0, 1.0, 1.0,],
                                 dtype = numpy.float32)

        ### unbind vao and vbo
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindVertexArray(0)

        ### create VAO
        self.__bufferVAO = glGenVertexArrays(1)
        glBindVertexArray(self.__bufferVAO)

        ### create a VBO for position and uv
        posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation)
        glVertexAttribPointer(self.__vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        # uncomment these
        #glEnableVertexAttribArray(self.__texCoordLocation)
        #glVertexAttribPointer(self.__texCoordLocation, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(96))

        ### create VBO for color
        colVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colVBO)
        glBufferData(GL_ARRAY_BUFFER, colorData.nbytes, colorData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__colorLocation)
        glVertexAttribPointer(self.__colorLocation,    4, GL_FLOAT, GL_FALSE, 0, None)

        ### unbind vao and vbo
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)




    ### DRAW BUFFER !!!
    def paintGL(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):

        #self.prepareFrameRect(x_offset, y_offset, frame_width, frame_height, zoom_factor)

        # http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-14-render-to-texture/
        #frame_buffer = glGenFramebuffers(1)
        #glBindFramebuffer(GL_DRAW_FRAMEBUFFER, frame_buffer)
        #glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)




        ### DRAW BACK
        self.__shaderProgram.setUniformValue(self.__use_color_location, 1.0)
        ### bind VAO
        glBindVertexArray(self.__bufferVAO)
        ### draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 18)

        glBindVertexArray(0)

        ### DRAW SOMETHING
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        ### bind texture
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        ### bind VAO
        glBindVertexArray(self.__VAO)
        ### draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 18)

         ### unbind
        glBindVertexArray(0)
        #glUseProgram(0)


        ### unbind
        glBindVertexArray(0)
        glUseProgram(0)



