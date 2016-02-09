
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

# http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-14-render-to-texture/
#frame_buffer = glGenFramebuffers(1)
#glBindFramebuffer(GL_DRAW_FRAMEBUFFER, frame_buffer)
#glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

### songho FBO
# http://www.songho.ca/opengl/gl_fbo.html

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

        self.__VAO = None
        self.__bufferVAO = None

    def initializeGL(self, ori_tex):




        ### texture
        self.__ori_tex = ori_tex

        vertexData = numpy.array([-30.0, -30.0, 0.0, 1.0,  # top left
                                  -20.0, 250.0, 0.0, 1.0,  # bottom left
                                  290.0, 290.0, 0.0, 1.0,  # bottom right
                                  -30.0, -30.0, 0.0, 1.0,  # top left
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
        if self.__VAO is None:
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

        #print xLeft, " ", yTop

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

        ### unbind vao and vbo
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindVertexArray(0)

        ### create VAO
        if self.__bufferVAO is None:
            self.__bufferVAO = glGenVertexArrays(1)

        glBindVertexArray(self.__bufferVAO)

        ### create a VBO for position and uv
        posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation)
        glVertexAttribPointer(self.__vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        # uncomment these
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




    ### DRAW BUFFER !!!
    def paintGL(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):

        self.prepareFrameRect(x_offset, y_offset, frame_width, frame_height, zoom_factor)



        #render_buffer = glGenRenderbuffers(1)
        #glBindRenderbuffer(GL_RENDERBUFFER, render_buffer)
        # read this: https://www.opengl.org/wiki/Framebuffer_Object_Examples
        # render_buffer = glGenRenderbuffers(1)
        #frame_buffer = glGenFramebuffers(1)
        #print frame_buffer
        #glBindFramebuffer(GL_DRAW_FRAMEBUFFER, frame_buffer)
        #glClearColor(0.0, 0.0, 0.0, 0.0)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
        #glDeleteFramebuffers(1, [frame_buffer])
        #glDeleteRenderbuffers(1, [render_buffer])

        ### http://www.songho.ca/opengl/gl_fbo.html

        # create a texture object
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE) # automatic mipmap
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

        # create a renderbuffer object to store depth info
        rboId = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rboId)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, frame_width, frame_height)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        # create a framebuffer object
        fboId = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fboId)

        # attach the texture to FBO color attachment point
        glFramebufferTexture2D(GL_FRAMEBUFFER,        # 1. fbo target: GL_FRAMEBUFFER
                               GL_COLOR_ATTACHMENT0,  # 2. attachment point
                               GL_TEXTURE_2D,         # 3. tex target: GL_TEXTURE_2D
                               textureId,             # 4. tex ID
                               0)                    # 5. mipmap level: 0(base)

        # attach the renderbuffer to depth attachment point
        glFramebufferRenderbuffer(GL_FRAMEBUFFER,      # 1. fbo target: GL_FRAMEBUFFER
                                    GL_DEPTH_ATTACHMENT, # 2. attachment point
                                    GL_RENDERBUFFER,     # 3. rbo target: GL_RENDERBUFFER
                                    rboId)              # 4. rbo ID

        # check FBO status
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if(status is not GL_FRAMEBUFFER_COMPLETE):
            print "FBO shit"
            fboUsed = False

        # switch back to window-system-provided framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        ### DRAW JUNK !!!
        self.__shaderProgram.setUniformValue(self.__use_color_location, 1.0)
        #glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        glBindVertexArray(self.__bufferVAO) ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        #glBindTexture(GL_TEXTURE_2D, 0)    ### unbind
        #glBindVertexArray(0)               ### unbind


        ### DRAW SOMETHING
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)     ### bind texture
        glBindVertexArray(self.__VAO)       ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        glBindTexture(GL_TEXTURE_2D, 0)     ### unbind
        #glUseProgram(0)                    ### unbind



