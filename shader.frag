#version 330

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