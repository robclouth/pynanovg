import math

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

def draw_eyes(vg, x, y, w, h, mx, my, t):
    ex = w * 0.23
    ey = h * 0.5
    lx = x + ex
    ly = y + ey
    rx = x + w - ex
    ry = y + ey
    br = (ex if ex < ey else ey) * 0.5
    blink = 1 - (math.sin(t*0.5)**200)*0.8

    #bg = vg.LinearGradient(x,y+h*0.5, x+w*0.1, y+h, nvgRGBA(0,0,0,32), nvgRGBA(0,0,0,16))
    vg.beginPath()
    vg.ellipse(lx+3.0, ly+16.0, ex, ey)
    vg.ellipse(rx+3.0, ry+16.0, ex, ey)
    #vg.fillPaint(bg)
    vg.fillColor(0.8, 0.8, 0.8, 1.0)
    vg.fill()

    #bg = nvgLinearGradient(vg, x,y+h*0.25f,x+w*0.1f,y+h, nvgRGBA(220,220,220,255), nvgRGBA(128,128,128,255))
    vg.beginPath()
    vg.ellipse(lx, ly, ex, ey)
    vg.ellipse(rx, ry, ex, ey)
    #vg.fillPaint(bg)
    vg.fillColor(0.1, 0.1, 0.1, 1.0)
    vg.fill()

    dx = (mx - rx) / (ex * 10.0)
    dy = (my - ry) / (ey * 10.0)
    d = math.sqrt(dx*dx+dy*dy)
    if d > 1:
    	dx /= d
        dy /= d
    dx *= ex*0.4
    dy *= ey*0.5
    vg.beginPath()
    vg.ellipse(lx+dx,ly+dy+ey*0.25*(1-blink), br,br*blink)
    vg.fillColor(0.12, 0.12, 0.12, 1.0)
    vg.fill()

    dx = (mx - rx) / (ex * 10)
    dy = (my - ry) / (ey * 10)
    d = math.sqrt(dx*dx+dy*dy)
    if (d > 1.0):
    	dx /= d
        dy /= d
    dx *= ex*0.4
    dy *= ey*0.5
    vg.beginPath()
    vg.ellipse(rx+dx,ry+dy+ey*0.25*(1-blink), br,br*blink)
    vg.fillColor(0.12, 0.12, 0.12, 1.0)
    vg.fill()

    gloss = nvgRadialGradient(lx-ex*0.25f,ly-ey*0.5f, ex*0.1f,ex*0.75f, nvgRGBA(255,255,255,128), nvgRGBA(255,255,255,0))
    vg.beginPath(vg)
    vg.ellipse(lx,ly, ex,ey)
    vg.fillPaint(gloss)
    vg.fill(vg)

    gloss = nvgRadialGradient(rx-ex*0.25f,ry-ey*0.5f, ex*0.1f,ex*0.75f, nvgRGBA(255,255,255,128), nvgRGBA(255,255,255,0))
    vg.beginPath(vg)
    vg.ellipse(rx,ry, ex,ey)
    vg.fillPaint(gloss)
    vg.fill(vg)

class Demo(Base):
    def setup(self):
        Base.setup(self)
        self.vg = pynanovg.Context()

        self.vg.createFont(b'light', b'../nanovg/example/Roboto-Light.ttf')
        self.vg.createFont(b'regular', b'../nanovg/example/Roboto-Regular.ttf')
        self.vg.createFont(b'bold', b'../nanovg/example/Roboto-Bold.ttf')

        img = self.vg.createImage(b'../nanovg/example/images/image2.jpg', 0)

        #used for the graphs
        self.vg.createFont(b'sans', b'../nanovg/example/Roboto-Regular.ttf')

    def render(self):
        vg = self.vg
        width, height = self.width, self.height
        mx, my = self.mouse
        t = 1

        vg.beginFrame(width, height, float(width)/float(height))

        draw_eyes(vg, width - 250, 50, 150, 100, mx, my, t)
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
        pos = np.vstack((pos*5,2*pos+(np.sin(pos)*100))).T

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


        vg.endFrame()
        vg.restore()

    def teardown(self):
        self.vg.reset()
        Base.teardown(self)

if __name__ == '__main__':
    demo = Demo(1000, 600)
    demo.run()

