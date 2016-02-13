

"""
radhitya@uwaterloo.ca
"""

import numpy

from OpenGL.GL import *
from PyQt4 import QtOpenGL
from PyQt4.QtOpenGL import *
#from PyQt4 import QtGui
#from PyQt4.QtGui import *

from OpenGL.GL.framebufferobjects import *

"""
see this:
https://raw.githubusercontent.com/azer89/ComicsVectorizer/master/CVUserInterface/RenderUtility.cpp
void RenderUtility::DrawFullscreen
"""

### ???
# http://stackoverflow.com/questions/8016050/pyqt-with-interactive-svg-images

### render svg using frame buffer
# https://github.com/RSATom/Qt/tree/master/qtsvg/examples/svg/opengl

### parse with something and render using qt
# http://stackoverflow.com/questions/1359003/svg-example-in-c-c

class MyBufferPainter(object):

    def __init__(self):
        print "MyBufferPainter"

    def SetThings(self, shaderProgram, blurProgram):
        self.__shaderProgram = shaderProgram
        self.__texCoordLocation   = self.__shaderProgram.attributeLocation("uv")
        self.__vertexLocation     = self.__shaderProgram.attributeLocation("position")
        self.__colorLocation      = self.__shaderProgram.attributeLocation("color")
        self.__use_color_location = self.__shaderProgram.uniformLocation("use_color")
        self.__mvpMatrixLocation  = self.__shaderProgram.uniformLocation("mvpMatrix")

        self.__blurProgram = blurProgram
        self.__texCoordLocation2   = self.__blurProgram.attributeLocation("uv")
        self.__vertexLocation2     = self.__blurProgram.attributeLocation("position")

        self.__colorLocation2      = self.__blurProgram.attributeLocation("color")
        self.__use_color_location2 = self.__blurProgram.uniformLocation("use_color")
        self.__mvpMatrixLocation2  = self.__blurProgram.uniformLocation("mvpMatrix")
        self.__blurResXLoc = self.__blurProgram.uniformLocation("resolutionx")
        self.__blurResYLoc = self.__blurProgram.uniformLocation("resolutiony")
        self.__blurRadiusLoc = self.__blurProgram.uniformLocation("radius")
        self.__blurDirXLoc = self.__blurProgram.uniformLocation("dirx")
        self.__blurDirYLoc = self.__blurProgram.uniformLocation("diry")

        print self.__texCoordLocation2, " ", self.__vertexLocation2, " ", self.__mvpMatrixLocation2
        print self.__blurResXLoc, " ", self.__blurResYLoc, " ", self.__blurRadiusLoc, " ", self.__blurDirXLoc, " ", self.__blurDirYLoc

        self.__VAO = None
        self.__bufferVAO = None

        self.__VAO2 = None
        self.__bufferVAO2 = None

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

        ### create VAO
        if self.__VAO2 is None:
            self.__VAO2 = glGenVertexArrays(1)

        glBindVertexArray(self.__VAO2)

        ### create a VBO for position and uv
        posVBO2 = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO2)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)

        glEnableVertexAttribArray(self.__vertexLocation2)
        glVertexAttribPointer(self.__vertexLocation2, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self.__texCoordLocation2)
        glVertexAttribPointer(self.__texCoordLocation2, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(96))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)




    def prepareFrameRect(self, x_offset, y_offset, frame_width, frame_height, zoom_factor):
        xLeft  = 0 + x_offset
        xRight = frame_width + x_offset

        yTop    = 0 + y_offset
        yBottom = frame_height + y_offset

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

        ### create VAO
        if self.__bufferVAO2 is None:
            self.__bufferVAO2 = glGenVertexArrays(1)

        glBindVertexArray(self.__bufferVAO2)

        ### create a VBO for position and uv
        posVBO2 = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, posVBO2)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.__vertexLocation2)
        glVertexAttribPointer(self.__vertexLocation2, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self.__texCoordLocation2)
        glVertexAttribPointer(self.__texCoordLocation2, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(96))

        ### unbind vao and vbo
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    ### DRAW BUFFER !!!
    def paintGL(self, x_offset, y_offset, frame_width, frame_height, zoom_factor, mpvMatrix):

        self.prepareFrameRect(x_offset, y_offset, frame_width, frame_height, zoom_factor)
        self.prepareShitTonsOfBuffers(frame_width, frame_height)

        #self.__shaderProgram.bind()
        #self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)
        self.__blurProgram.bind()
        self.__blurProgram.setUniformValue(self.__mvpMatrixLocation2, mpvMatrix)

        #print self.__texCoordLocation2, " ", self.__vertexLocation2, " ", self.__mvpMatrixLocation2
        #print self.__blurResXLoc, " ", self.__blurResYLoc, " ", self.__blurRadiusLoc, " ", self.__blurDirXLoc, " ", self.__blurDirYLoc

        #self.__blurProgram.setUniformValue(self.__blurRadiusLoc, 1.0 / zoom_factor)
        #self.__blurProgram.setUniformValue(self.__blurResXLoc, frame_width)
        #self.__blurProgram.setUniformValue(self.__blurDirXLoc, 1.0)
        #self.__blurProgram.setUniformValue(self.__blurDirYLoc, 0.0)

        glBindFramebuffer(GL_FRAMEBUFFER, self.__fboId3)

        ###  clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ### DRAW JUNK !!!
        #self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        self.__blurProgram.setUniformValue(self.__use_color_location2, 0.0)
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        glBindVertexArray(self.__bufferVAO) ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        #glBindTexture(GL_TEXTURE_2D, 0)    ### unbind
        #glBindVertexArray(0)               ### unbind

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        #self.__shaderProgram.release()
        self.__blurProgram.release()


        # self.__shaderProgram.bind()
        # self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)
        self.__blurProgram.bind()
        self.__blurProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)

        ### DRAW SOMETHING
        #self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        self.__blurProgram.setUniformValue(self.__use_color_location, 0.0)
        #glBindTexture(GL_TEXTURE_2D, self.__ori_tex)     ### bind texture
        glBindTexture(GL_TEXTURE_2D, self.__bufTextureId3)
        glBindVertexArray(self.__VAO)       ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        glBindTexture(GL_TEXTURE_2D, 0)     ### unbind
        #glUseProgram(0)                    ### unbind

        #self.__shaderProgram.release()
        self.__blurProgram.release()



    """
    ### DRAW BUFFER !!!
    def paintGL(self, x_offset, y_offset, frame_width, frame_height, zoom_factor, mpvMatrix):

        self.prepareFrameRect(x_offset, y_offset, frame_width, frame_height, zoom_factor)
        self.prepareShitTonsOfBuffers(frame_width, frame_height)

        self.__shaderProgram.bind()
        self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)
        #self.__blurProgram.bind()
        #self.__blurProgram.setUniformValue(self.__mvpMatrixLocation2, mpvMatrix)

        #print self.__texCoordLocation2, " ", self.__vertexLocation2, " ", self.__mvpMatrixLocation2
        #print self.__blurResXLoc, " ", self.__blurResYLoc, " ", self.__blurRadiusLoc, " ", self.__blurDirXLoc, " ", self.__blurDirYLoc

        #self.__blurProgram.setUniformValue(self.__blurRadiusLoc, 1.0 / zoom_factor)
        #self.__blurProgram.setUniformValue(self.__blurResXLoc, frame_width)
        #self.__blurProgram.setUniformValue(self.__blurDirXLoc, 1.0)
        #self.__blurProgram.setUniformValue(self.__blurDirYLoc, 0.0)

        glBindFramebuffer(GL_FRAMEBUFFER, self.__fboId3)

        ###  clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ### DRAW JUNK !!!
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        glBindTexture(GL_TEXTURE_2D, self.__ori_tex)
        glBindVertexArray(self.__bufferVAO) ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        #glBindTexture(GL_TEXTURE_2D, 0)    ### unbind
        #glBindVertexArray(0)               ### unbind

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.__shaderProgram.release()
        #self.__blurProgram.release()


        self.__shaderProgram.bind()
        self.__shaderProgram.setUniformValue(self.__mvpMatrixLocation, mpvMatrix)

        ### DRAW SOMETHING
        self.__shaderProgram.setUniformValue(self.__use_color_location, 0.0)
        #glBindTexture(GL_TEXTURE_2D, self.__ori_tex)     ### bind texture
        glBindTexture(GL_TEXTURE_2D, self.__bufTextureId3)
        glBindVertexArray(self.__VAO)       ### bind VAO
        glDrawArrays(GL_TRIANGLES, 0, 6)    ### draw triangle
        glBindVertexArray(0)                ### unbind
        glBindTexture(GL_TEXTURE_2D, 0)     ### unbind
        #glUseProgram(0)                    ### unbind

        self.__shaderProgram.release()
    """


    def prepareShitTonsOfBuffers(self, frame_width, frame_height):
        """
        http://www.songho.ca/opengl/gl_fbo.html
        """

        ### FIRST FBO
        ### create a texture object
        self.__bufTextureId1 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__bufTextureId1)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)

        ### create a renderbuffer object to store depth info
        self.__rboId1 = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__rboId1)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, frame_width, frame_height)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        ### create a framebuffer object
        self.__fboId1 = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__fboId1)

        ### attach the texture to FBO color attachment point
        glFramebufferTexture2D(GL_FRAMEBUFFER,        # 1. fbo target: GL_FRAMEBUFFER
                               GL_COLOR_ATTACHMENT0,  # 2. attachment point
                               GL_TEXTURE_2D,         # 3. tex target: GL_TEXTURE_2D
                               self.__bufTextureId1,  # 4. tex ID
                               0)                     # 5. mipmap level: 0(base)

        ### attach the renderbuffer to depth attachment point
        glFramebufferRenderbuffer(GL_FRAMEBUFFER,      # 1. fbo target: GL_FRAMEBUFFER
                                    GL_DEPTH_ATTACHMENT, # 2. attachment point
                                    GL_RENDERBUFFER,     # 3. rbo target: GL_RENDERBUFFER
                                    self.__fboId1)              # 4. rbo ID

        ### check FBO status
        fstatus = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if(fstatus != GL_FRAMEBUFFER_COMPLETE):
            print "FBO 1 shit"
        #else:
        #    print "FBO 1 ok"

        ### switch back to window-system-provided framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


        ### SECOND FBO
        ### create a texture object
        self.__bufTextureId2 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__bufTextureId2)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)

        ### create a renderbuffer object to store depth info
        self.__rboId2 = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__rboId2)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, frame_width, frame_height)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        ### create a framebuffer object
        self.__fboId2 = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__fboId2)

        ### attach the texture to FBO color attachment point
        glFramebufferTexture2D(GL_FRAMEBUFFER,        # 1. fbo target: GL_FRAMEBUFFER
                               GL_COLOR_ATTACHMENT0,  # 2. attachment point
                               GL_TEXTURE_2D,         # 3. tex target: GL_TEXTURE_2D
                               self.__bufTextureId2,  # 4. tex ID
                               0)                     # 5. mipmap level: 0(base)

        ### attach the renderbuffer to depth attachment point
        glFramebufferRenderbuffer(GL_FRAMEBUFFER,      # 1. fbo target: GL_FRAMEBUFFER
                                    GL_DEPTH_ATTACHMENT, # 2. attachment point
                                    GL_RENDERBUFFER,     # 3. rbo target: GL_RENDERBUFFER
                                    self.__rboId2)              # 4. rbo ID

        ### check FBO status
        fstatus = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if(fstatus != GL_FRAMEBUFFER_COMPLETE):
            print "FBO 2 shit"
        #else:
        #    print "FBO 2 ok"

        ### switch back to window-system-provided framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)



        ### http://www.songho.ca/opengl/gl_fbo.html
        ### create a texture object
        self.__bufTextureId3 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__bufTextureId3)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)

        ### create a renderbuffer object to store depth info
        self.__rboId3 = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__rboId3)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, frame_width, frame_height)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        ### create a framebuffer object
        self.__fboId3 = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__fboId3)

        ### attach the texture to FBO color attachment point
        glFramebufferTexture2D(GL_FRAMEBUFFER,        # 1. fbo target: GL_FRAMEBUFFER
                               GL_COLOR_ATTACHMENT0,  # 2. attachment point
                               GL_TEXTURE_2D,         # 3. tex target: GL_TEXTURE_2D
                               self.__bufTextureId3,             # 4. tex ID
                               0)                    # 5. mipmap level: 0(base)

        ### attach the renderbuffer to depth attachment point
        glFramebufferRenderbuffer(GL_FRAMEBUFFER,      # 1. fbo target: GL_FRAMEBUFFER
                                    GL_DEPTH_ATTACHMENT, # 2. attachment point
                                    GL_RENDERBUFFER,     # 3. rbo target: GL_RENDERBUFFER
                                    self.__rboId3)              # 4. rbo ID

        ### check FBO status
        fstatus = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if(fstatus != GL_FRAMEBUFFER_COMPLETE):
            print "FBO 3 shit"
        #else:
        #    print "FBO 3 ok"

        ### switch back to window-system-provided framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)




