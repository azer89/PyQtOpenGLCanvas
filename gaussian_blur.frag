#version 330

in vec2 theUV;
in vec4 theColor;
out vec4 outputColor;

uniform float use_color;
uniform sampler2D base_texture;


uniform float resolutionx;
uniform float resolutiony;
uniform float radius;
uniform float dirx;
uniform float diry;


void main(void)
{
    // delete this !!!
    outputColor = texture2D(base_texture, theUV);
    if(use_color > 0.5)
    {
     	outputColor = theColor;
    }
    // delete this !!!

	vec2 dir = vec2(dirx, diry);
    vec4 sum = vec4(0.0, 0.0, 0.0, 0.0);
    vec2 tc = theUV;

	float hstep = dir.x * radius / resolutionx;
    float vstep = dir.y * radius / resolutiony;

	vec4 texColor = texture2D(base_texture, tc);

	sum += texture2D(base_texture, vec2(tc.x - 4.0 * hstep, tc.y - 4.0 * vstep )) * 0.0162162162;
    sum += texture2D(base_texture, vec2(tc.x - 3.0 * hstep, tc.y - 3.0 * vstep )) * 0.0540540541;
    sum += texture2D(base_texture, vec2(tc.x - 2.0 * hstep, tc.y - 2.0 * vstep )) * 0.1216216216;
    sum += texture2D(base_texture, vec2(tc.x - 1.0 * hstep, tc.y - 1.0 * vstep )) * 0.1945945946;

    sum += texture2D(base_texture, vec2(tc.x, tc.y)) * 0.2270270270;

    sum += texture2D(base_texture, vec2(tc.x + 1.0 * hstep, tc.y + 1.0 * vstep )) * 0.1945945946;
    sum += texture2D(base_texture, vec2(tc.x + 2.0 * hstep, tc.y + 2.0 * vstep )) * 0.1216216216;
    sum += texture2D(base_texture, vec2(tc.x + 3.0 * hstep, tc.y + 3.0 * vstep )) * 0.0540540541;
    sum += texture2D(base_texture, vec2(tc.x + 4.0 * hstep, tc.y + 4.0 * vstep )) * 0.0162162162;

	//outputColor = sum;


}