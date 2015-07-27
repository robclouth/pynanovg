
def draw(vg):

    # test font rendering
    txt = b'Hello World - From submodule'
    # print vg.textBounds(0,0,txt)
    # print vg.textMetrics(1.)
    # print vg.textBreakLines(txt)

    vg.fontFace(b'light')
    vg.fontSize(24.0)
    vg.fillColor( 1.0, 0.0, 1.0, 1.0 )
    vg.text(15.0, 230.0, txt)
