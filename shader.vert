#version 330

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