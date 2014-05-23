#source: https://gist.github.com/tito/4250317
from kivy.graphics import Fbo, Rectangle, Color
from kivy.graphics.opengl import glFinish
 
def radial_gradient(border_color=(1, 1, 0), center_color=(1, 0, 0),
        size=(64, 64)):
    fbo = Fbo(size=size)
    fbo.shader.fs = '''
    $HEADER$
    uniform vec3 border_color;
    uniform vec3 center_color;
    void main (void) {
        float d = clamp(distance(tex_coord0, vec2(0.5, 0.5)), 0., 1.);
        gl_FragColor = vec4(mix(center_color, border_color, d), 1);
    }
    '''
 
    # use the shader on the entire surface
    fbo['border_color'] = [float(x) for x in  border_color]
    fbo['center_color'] = [float(x) for x in  center_color]
    with fbo:
        Color(1, 1, 1)
        Rectangle(size=size)
    fbo.draw()
    return fbo.texture