import logging

import numpy as np
import pynanovg

import time

from base import Base

def draw_lines(x, y, w):
    for i in range(1000):
        sw = (i+0.05)*.1
        vg.strokeWidth(sw)
        vg.beginPath()
        vg.moveTo(x,y)
        vg.lineTo(x+1000.,y)
        vg.stroke()
        y += 1.

class Demo(Base):

    def setup(self):
        Base.setup(self)
        self.vg = pynanovg.Context()

        #nanovg.create_shared_context() # only needs to be called once per process.
        #from nanovg import vg, colorRGBAf,GRAPH_RENDER_FPS,GRAPH_RENDER_PERCENT
        self.vg.createFont(b'light', b'../nanovg/example/Roboto-Light.ttf')
        self.vg.createFont(b'regular', b'../nanovg/example/Roboto-Regular.ttf')
        self.vg.createFont(b'bold', b'../nanovg/example/Roboto-Bold.ttf')

        img = self.vg.createImage(b'../nanovg/example/images/image2.jpg', 0)

        #used for the graphs
        self.vg.createFont(b'sans', b'../nanovg/example/Roboto-Regular.ttf')
        #fps = nanovg.Graph(vg,GRAPH_RENDER_FPS,"Framerate")
        #fps.pos= (20,20)
        #cpu = nanovg.Graph(vg,GRAPH_RENDER_PERCENT,"CPU load of Process")
        #cpu.pos = (240,20)
        ts = time.time()


    def render(self):
        vg = self.vg
        width, height = self.width, self.height
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

        pos = np.arange(0, 10, .1, dtype=np.float)
        print(len(pos))
        pos = np.vstack((pos*5,2*pos+(np.sin(pos)*100))).T
        print(pos.shape)

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

        #import os
        #import psutil

        # pid = os.getpid()
        # ps = psutil.Process(pid)

    def teardown(self):
        self.vg.reset()
        Base.teardown(self)


if __name__ == '__main__':
    demo = Demo(1000, 600)
    demo.run()

