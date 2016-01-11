import sys
import numpy
from OpenGL.GL import *

from PyQt4.QtGui import QWidget
from PyQt4 import QtGui, QtCore

from PyQt4 import QtGui, QtOpenGL

from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
#from PyQt4.QtOpenGL import QGLShaderProgram, QGLShader
#from PyQt4.QtGui import QMatrix4x4


vertex_shader = """#version 330
in vec2 uv;
in vec4 position;
in vec4 color;
out vec2 theUV;
out vec4 theColor;
uniform mat4 mvpMatrix;
void main()
{
    gl_Position = mvpMatrix * position;
    theUV = uv;
    theColor = color;
}
"""


fragment_shader = """#version 330
in vec2 theUV;
in vec4 theColor;
out vec4 outputColor;
uniform float use_color;
uniform sampler2D base_texture;
void main()
{
    outputColor = texture2D(base_texture, theUV);
    if(use_color > 0.5)
    {
     	outputColor = theColor;
    }
}
"""


class GLWidget(QtOpenGL.QGLWidget):
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


    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glViewport(0, 0, self.width(), self.height())

        self._shaderProgram = QGLShaderProgram()

        if self._shaderProgram.addShaderFromSourceCode(QGLShader.Vertex, vertex_shader) :
            print "Vertex shader OK"

        if self._shaderProgram.addShaderFromSourceCode(QGLShader.Fragment, fragment_shader) :
            print "Fragment shader OK"

        # texture
        self._ori_tex = self.bindTexture(QtGui.QPixmap("laughing_man.png"))

        self._shaderProgram.link()

        self._texCoordLocation   = self._shaderProgram.attributeLocation("uv")
        self._vertexLocation     = self._shaderProgram.attributeLocation("position")
        self._colorLocation      = self._shaderProgram.attributeLocation("color")

        self._use_color_location = self._shaderProgram.uniformLocation("use_color")
        self._mvpMatrixLocation  = self._shaderProgram.uniformLocation("mvpMatrix")

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
        glEnableVertexAttribArray(self._vertexLocation)
        glVertexAttribPointer(self._vertexLocation, 4, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(self._texCoordLocation)
        glVertexAttribPointer(self._texCoordLocation, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(48))

        # create VBO for color
        colVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colVBO)
        glBufferData(GL_ARRAY_BUFFER, colorData.nbytes, colorData, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self._colorLocation)
        glVertexAttribPointer(self._colorLocation,    4, GL_FLOAT, GL_FALSE, 0, None)

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
        self._shaderProgram.bind()
        self._shaderProgram.setUniformValue(self._use_color_location, 0.0)
        glBindTexture(GL_TEXTURE_2D, self._ori_tex)
        self._shaderProgram.setUniformValue(self._mvpMatrixLocation, mpvMatrix)

        glBindVertexArray(self.VAO)

        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 9)

        glBindVertexArray(0)
        glUseProgram(0)