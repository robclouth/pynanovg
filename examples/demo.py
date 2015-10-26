import logging

import numpy as np
import glfw
import OpenGL
from OpenGL.GL import *
import pynanovg

# create logger for the context of this function
logger = logging.getLogger(__name__)

import time

width, height = (1000, 600)

def basic_gl_setup():
    glEnable( GL_POINT_SPRITE )
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE) # overwrite pointsize
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glClearColor(0., 0., 0., 1.0)

def adjust_gl_view(w,h,window):
    """
    adjust view onto our scene.
    """
    h = max(h,1)
    w = max(w,1)

    hdpi_factor = glfwGetFramebufferSize(window)[0]/glfwGetWindowSize(window)[0]
    w,h = w*hdpi_factor,h*hdpi_factor
    glViewport(0, 0, w, h)

def clear_gl_screen():
    glClearColor(0.7, 0.7, 0.7, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT)

def demo():
    global quit
    quit = False

    # Callback functions
    def on_resize(window,w, h):
        active_window = glfw.get_current_context()
        glfw.make_context_current(window)
        # norm_size = normalize((w,h),glfwGetWindowSize(window))
        # fb_size = denormalize(norm_size,glfwGetFramebufferSize(window))
        adjust_gl_view(w,h,window)
        glfw.make_context_current(active_window)
        global width
        global height
        width,height = w,h

    def on_key(window, key, scancode, action, mods):
        # print "key pressed: ", key
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                on_close(window)

    def on_button(window,button, action, mods):
        pos = glfw.get_cursor_pos(window)
        # pos = normalize(pos,glfwGetWindowSize(window))
        # pos = denormalize(pos,(frame.img.shape[1],frame.img.shape[0]) ) # Position in img pixels

    def on_close(window):
        global quit
        quit = True
        logger.info('Process closing from window')

    def draw_lines(x, y, w):
        for i in range(1000):
            sw = (i+0.05)*.1
            vg.strokeWidth(sw)
            vg.beginPath()
            vg.moveTo(x,y)
            vg.lineTo(x+1000.,y)
            vg.stroke()
            y += 1.

    def draw_bezier():
        pass

    # get glfw started
    glfw.init()
    window = glfw.create_window(width, height, "Python NanoVG Demo", None, None)
    glfw.set_window_pos(window,0,0)

    # Register callbacks window
    glfw.set_window_size_callback(window, on_resize)
    glfw.set_window_close_callback(window, on_close)
    glfw.set_key_callback(window, on_key)
    glfw.set_mouse_button_callback(window, on_button)

    basic_gl_setup()

    # glfwSwapInterval(0)
    glfw.make_context_current(window)

    vg = pynanovg.Context()
    #nanovg.create_shared_context() # only needs to be called once per process.
    #from nanovg import vg, colorRGBAf,GRAPH_RENDER_FPS,GRAPH_RENDER_PERCENT
    vg.createFont(b'light', b'../nanovg/example/Roboto-Light.ttf')
    vg.createFont(b'regular', b'../nanovg/example/Roboto-Regular.ttf')
    vg.createFont(b'bold', b'../nanovg/example/Roboto-Bold.ttf')

    img = vg.createImage(b'../nanovg/example/images/image2.jpg', 0)

    pos = np.arange(0,10,.1,dtype=np.float)
    print(len(pos))
    pos = np.vstack((pos*5,2*pos+(np.sin(pos)*100))).T
    print(pos.shape)

    #used for the graphs
    vg.createFont(b'sans', b'../nanovg/example/Roboto-Regular.ttf')
    #fps = nanovg.Graph(vg,GRAPH_RENDER_FPS,"Framerate")
    #fps.pos= (20,20)
    #cpu = nanovg.Graph(vg,GRAPH_RENDER_PERCENT,"CPU load of Process")
    #cpu.pos = (240,20)
    ts = time.time()

    #import os
    #import psutil

    # pid = os.getpid()
    # ps = psutil.Process(pid)

    import loaded_module

    while not quit:
        clear_gl_screen()
        # show some nanovg graphics

        vg.beginFrame(width, height, float(width)/float(height))
        # draw_lines(0.,0.,100.)
        # res = vg.textBounds(0.0, 0.0, "here is my text", "t")
        # vg.save()
        # draw rect
        #p = vg.linearGradient(0.0, 0.0, 1000.0, 600.0, colorRGBAf(0.0,0.0,1.0,1.0), colorRGBAf(0.,1.,0.2,0.5))
        # rg = vg.radialGradient(0.0, 0.0, 100.0, 120.0, colorRGBAf(0.0,0.0,1.0,1.0), colorRGBAf(0.,1.,0.2,0.5))
        vg.beginPath()
        # vg.fillColor(colorRGBAf(0.2,0.2,0.2,0.4))
        vg.roundedRect(10.0, 10.0, 490.0, 290.0, 5.0)

        #vg.fillPaint(p)
        vg.fillColor(1.0, 0.0, 0.0, 0.8)
        vg.fill()

        #rg = vg.linearGradient(500.0, 300.0, 100.0, 200.0, colorRGBAf(0.0,0.0,0.0,0.0), colorRGBAf(0.,1.,0.2,0.5))
        vg.beginPath()
        #vg.fillPaint(rg)
        vg.fillColor(0.0, 1.0, 0.0, 0.8)
        vg.strokeColor(0.0, 0.4, 0.7, 0.9)
        vg.strokeWidth(2.0)

        #if 0:
        vg.beginPath()
        vg.moveTo(100,100)
        for x,y in pos:
            vg.lineTo(x,y)

        #else:
        #    # pass
        #    vg.Polyline(pos)

        vg.fill()
        vg.stroke()
        loaded_module.draw(vg)
        # test font rendering
        txt = b'Hello World - Python NanoVG bindings.'
        # print vg.textBounds(0,0,txt)
        # print vg.textMetrics(1.)
        # print vg.textBreakLines(txt)

        vg.fontFace(b'bold')
        vg.fontSize(24.0)
        vg.fillColor(0.0, 0.0, 0.0, 0.9)
        vg.text(15.0, 30.0, txt)

        vg.fontFace(b'regular')
        vg.fillColor(1.0, 1.0, 1.0, 1.0)
        vg.text(15.0, 50.0, txt)

        vg.fontFace(b'light')
        vg.fillColor(0.0,1.0,0.2,1.0)
        vg.text(15.0, 70.0, txt)
        # print random.random()
        #dt,ts = time.time()-ts,time.time()
        # print dt
        #fps.update(dt)
        #fps.render()


        #pct = ps.get_cpu_percent()
        # pct = psutil.cpu_percent()
        #cpu.update(pct)
        #cpu.render()
        vg.endFrame()
        vg.restore()
        glfw.swap_buffers(window)
        glfw.poll_events()
        # time.sleep(.03)

    vg.reset()
    glfw.destroy_window(window)
    glfw.terminate()
    logger.debug("Process done")

if __name__ == '__main__':
    demo()

