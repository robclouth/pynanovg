# distutils: sources = nanovg/src/nanovg.c

cimport cnanovg as nvg

import cython
import numpy as np
cimport numpy as np
DTYPE = np.float
ctypedef np.float_t DTYPE_t

class NVGError(Exception):
    """General Exception for this module"""
    def __init__(self, arg):
        super(NVGError, self).__init__()
        self.arg = arg

#
# context class holds nanovg graphics context pointer and provides drawing methods
#
cdef class Context:
    cdef nvg.NVGcontext *ctx

    def __cinit__(self):
        # todo - handle other backends like gl3 or gles
        self.ctx = nvg.nvgCreateGL3(nvg.NVG_ANTIALIAS | nvg.NVG_STENCIL_STROKES)
        if self.ctx is NULL:
            raise NVGError("Could not create NVG Context")

    def __dealloc__(self):
        if self.ctx:
            nvg.nvgDeleteGL3(self.ctx)

    def __repr__(self):
        return "NanoVG context"


    #####################################################
    # Begin drawing a new frame
    # calls to nanovg drawing API should be wrapped in beginFrame() and endFrame()
    #####################################################
    def beginFrame(self, int window_w, int window_h, float pix_ratio):
        '''
        nvgBeginframe() defines the size of the window to render to in relation to the current viewport
        i.e. glViewport on GL backends
        Device pixel ratio allows for control on Hi-DPI devices (like retina screens)
        For example, if GLFW returns two dimensions for an opened window: window size and frame buffer size
        In that case you would change the pix ratio from: windowWidth/windowHeight to the frameBufferWidth/windowWidth
        '''
        nvg.nvgBeginFrame(self.ctx, window_w, window_h, pix_ratio)

    def endFrame(self):
        '''
        ends drawing and flushes remaining render state
        '''
        nvg.nvgEndFrame(self.ctx)


    #####################################################
    # State Handling
    # NanoVG contains state which represents how paths will be rendered.
    # The state contains transform, fill and stroke styles, text and font styles,
    # and scissor clipping.
    #####################################################
    def save(self):
        '''
        Pushes and saves the current render state into a state stack
        A matching restore() must be used to restore the state
        '''
        nvg.nvgSave(self.ctx)

    def restore(self):
        '''
        Pops and restores the current render state
        '''
        nvg.nvgRestore(self.ctx)

    def reset(self):
        '''
        Resets the current render state to default values
        Does not affect the render state stack
        '''
        nvg.nvgReset(self.ctx)


    #####################################################
    # Render Styles
    # Fill & stroke can either be solid color or a paint - which is a gradient or pattern
    # - Solid color is defined by a color value
    # - Different kinds of paints can be created using gradients or patterns
    # - Save render styles with save() and restore()
    #####################################################
    def shapeAntiAlias(self, int enabled):
        '''
        Sets whether to draw antialias
        '''
        nvg.nvgShapeAntiAlias(self.ctx, enabled)


    def strokeColor(self, float r=0.0, float g=0.0, float b=0.0, float a=0.0):
        '''
        set current stroke to a solid color with or w/o alpha def by color
        '''
        cdef nvg.NVGcolor _color = nvg.NVGcolor(r, g, b, a)
        nvg.nvgStrokeColor(self.ctx, _color)

    def strokePaint(self, nvg.NVGpaint paint):
        '''
        set current stroke style to a paint type
        - gradient (or)
        - pattern
        '''
        nvg.nvgStrokePaint(self.ctx, paint)

    def fillColor(self, float r=0.0, float g=0.0, float b=0.0, float a=0.0):
        '''
        set current fill to a solid color with or w/o alpha def by color
        '''
        cdef nvg.NVGcolor _color = nvg.NVGcolor(r, g, b, a)
        nvg.nvgFillColor(self.ctx, _color)

    def fillPaint(self, nvg.NVGpaint paint):
        '''
        set current fill style to a paint type
        - gradient (or)
        - pattern
        '''
        nvg.nvgFillPaint(self.ctx, paint)

    def miterLimit(self, float limit):
        '''
        sets the miter limit of the stroke style
        miter limit controls when a sharp corner is beveled
        '''
        nvg.nvgMiterLimit(self.ctx, limit)

    def strokeWidth(self, float w):
        '''
        Sets the stroke width of the stroke style in pixels
        '''
        nvg.nvgStrokeWidth(self.ctx, w)

    def lineCap(self, int cap):
        '''
        sets how the end of the line (cap) is drawn
        - NVG_BUTT (default)    = 1
        - NVG_ROUND             = 2
        - NVG_SQUARE            = 3
        '''
        nvg.nvgLineCap(self.ctx, cap)

    def lineJoin(self, int join):
        '''
        sets how sharp the path corners are drawn
        - NVG_MITER (default)   = 1
        - NVG_ROUND             = 2
        - NVG_BEVEL             = 3
        '''
        nvg.nvgLineJoin(self.ctx, join)

    def globalAlpha(self, float alpha):
        '''
        sets the transparency applied to all rendered shapes
        already transparent paths will get proportinally more transparent as well
        '''
        nvg.nvgGlobalAlpha(self.ctx, alpha)


    #####################################################
    # Transforms
    #
    # The paths, gradients, patterns and scissor region are
    # transformed by a transformation matrix at the time when they are passed to the API.
    # The current transformation matrix is a affine matrix:
    #   [sx kx tx]
    #   [ky sy ty]
    #   [ 0  0  1]
    # Where: sx,sy define scaling, kx,ky skewing, and tx,ty translation.
    # The last row is assumed to be 0,0,1 and is not stored.
    #
    # Apart from nvgResetTransform(), each transformation function first creates
    # specific transformation matrix and pre-multiplies the current transformation by it.
    #
    # Current coordinate system (transformation) can be saved and restored using save() and restore().
    #####################################################
    def resetTransform(self):
        '''
        Resets current transform to a identity matrix.
        '''
        nvg.nvgResetTransform(self.ctx)

    def transform(self, float a, float b, float c, float d, float e, float f):
        '''
        Pre-multiplies current coordinate system by the specified matrix
        The parameters are interpreted in the following matrix:
        [a, c, e]
        [b, d, f]
        [0, 0, 1]
        '''
        # should this receive a numpy matrix instead 6 floats?
        nvg.nvgTransform(self.ctx, a, b, c, d, e, f)

    def translate(self, float x, float y):
        '''
        Translate the current coordinate system
        '''
        nvg.nvgTranslate(self.ctx, x, y)

    def rotate(self, float angle):
        '''
        Rotates the current coordinate system
        angle is specified in radians
        '''
        nvg.nvgRotate(self.ctx, angle)

    def skewX(self, float angle):
        '''
        skews the current coordinate system along the X axis
        angle is specified in radians
        '''
        nvg.nvgSkewX(self.ctx, angle)

    def skewY(self, float angle):
        '''
        skews the current coordinate system along the Y axis
        angle is specified in radians
        '''
        nvg.nvgSkewY(self.ctx, angle)

    def scale(self, float x, float y):
        '''
        scales the coordinate system
        '''
        nvg.nvgScale(self.ctx, x, y)

    # def currentTransform(self, xform):
    #     '''
    #     stores the top part a-f of the current transformation matrix to buffer
    #     '''
    #     cdef np.ndarray[np.float32_t, ndim=1, mode='c'] xf = np.zeros(6, dtype=np.float32)
    #     for i in range(xf.shape[0]):
    #         xf[i] = xform[i]
    #     # TODO - this should be a numpy array
    #     nvg.nvgCurrentTransform(self.ctx, xf)

    #####################################################
    # Functions for calculations on a 2x3 transformation matrix
    # -- TODO these do not require the context so should be done outside of class
    #####################################################

    #####################################################
    # Images
    # NanoVG allows you to load jpg, png, psd, tga, pic and gif files to be used for rendering.
    # In addition you can upload your own image. The image loading is provided by stb_image.
    #####################################################
    def build_image_flags(self, generate_mipmaps=False, repeat_x=False, repeat_y=False, flip_y=False, premultiplied=False, nearest=False):
        cdef int flags = 0
        if generate_mipmaps:
            flags |= nvg.NVG_IMAGE_GENERATE_MIPMAPS
        if repeat_x:
            flags |= nvg.NVG_IMAGE_REPEATX
        if repeat_y:
            flags |= nvg.NVG_IMAGE_REPEATY
        if flip_y:
            flags |= nvg.NVG_IMAGE_FLIPY
        if premultiplied:
            flags |= nvg.NVG_IMAGE_PREMULTIPLIED
        if nearest:
            flags |= nvg.NVG_IMAGE_NEAREST
        return flags

    def createImage(self, const char* filename, generate_mipmaps=False, repeat_x=False, repeat_y=False, flip_y=False, premultiplied=False, nearest=False):
        '''
        Creates image by loading it from the disk from specified file name.
        Returns handle to the image.
        '''
        imageFlags = self.build_image_flags(generate_mipmaps, repeat_x, repeat_y, flip_y, premultiplied, nearest)
        return <int>nvg.nvgCreateImage(self.ctx, filename, imageFlags)

    def createImageMem(self, unsigned char* data, int ndata, generate_mipmaps=False, repeat_x=False, repeat_y=False, flip_y=False, premultiplied=False, nearest=False):
        '''
        creates image by loading it from the specified chunk of memory
        returns handle to the image
        '''
        imageFlags = self.build_image_flags(generate_mipmaps, repeat_x, repeat_y, flip_y, premultiplied, nearest)
        return <int>nvg.nvgCreateImageMem(self.ctx, imageFlags, data, ndata)

    def createImageRGBA(self, int w, int h, const unsigned char* data, generate_mipmaps=False, repeat_x=False, repeat_y=False, flip_y=False, premultiplied=False, nearest=False):
        '''
        creates image from specified image data
        returns handle to the image
        '''
        imageFlags = self.build_image_flags(generate_mipmaps, repeat_x, repeat_y, flip_y, premultiplied, nearest)
        return <int>nvg.nvgCreateImageRGBA(self.ctx, w, h, imageFlags, data)

    def updateImage(self, int image, const unsigned char* data):
        '''
        updates image data specified by image handle
        '''
        nvg.nvgUpdateImage(self.ctx, image, data)

    def imageSize(self, int image):
        '''
        returns the dimensions of a created image
        '''
        cdef int width, height
        # width = &w
        # height = &h

        nvg.nvgImageSize(self.ctx, image, &width, &height)
        return (width, height)

    def deleteImage(self, int image):
        '''
        deletes image specified by image handle
        '''
        nvg.nvgDeleteImage(self.ctx, image)

    #####################################################
    # Paint
    # NanoVG supports four types of paints:
    # - linear gradient
    # - box gradient
    # - radial gradient
    # - image pattern.
    # Can be used as paints for strokes and fills.
    #####################################################
    def linearGradient(self, float sx, float sy, float ex, float ey, c0, c1):
        '''
        Creates and returns a linear gradient.
        - (sx,sy)-(ex,ey) specify the start and end coordinates of the linear gradient,
        - color0 specifies the start color
        - color1 specifies the end color
        The gradient is transformed by the current transform when it is passed to fillPaint() or strokePaint()
        '''
        cdef nvg.NVGcolor col0 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        cdef nvg.NVGcolor col1 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        return nvg.nvgLinearGradient(self.ctx, sx, sy, ex, ey, col0, col1)


    def boxGradient(self, float x, float y, float w, float h, float r, float f, c0, c1):
        '''
        Creates and returns a box gradient
        Box gradient is a feathered rounded rectangle
        useful for rendering drop shadows or highlights for boxes
        - (x,y) define the top-left corner of the rectangle
        - (w,h) define the size of the rectangle
        - r defines the corner radius
        - f feather - feather defines how blurry the border of the rectangle appears
        - color0 specifies the inner color of the gradient
        - color1 specifies the outer color of the gradient
        The gradient is transformed by the current transform when it is passed to fillPaint() or strokePaint().
        '''
        cdef nvg.NVGcolor col0 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        cdef nvg.NVGcolor col1 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        return nvg.nvgBoxGradient(self.ctx, x, y, w, h, r, f, col0, col1)


    cdef radialGradient(self, float cx, float cy, float inner, float outer, c0, c1):
        '''
        Creates and returns a radial gradient
        - (cx,cy) specify the center of the gradient
        - (inner, outer) specify the inner and outer radius of the gradient
        - color0, color1 specify the start and end color of the gradient
        The gradient is transformed by the current transform when it is passed to fillPaint() or strokePaint().
        '''
        cdef nvg.NVGcolor col0 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        cdef nvg.NVGcolor col1 = nvg.NVGcolor(c0[0], c0[1], c0[2], c0[3])
        return nvg.nvgRadialGradient(self.ctx, cx, cy, inner, outer, col0, col1)


    def imagePattern(self, float ox, float oy, float ex, float ey, float angle, int image, float alpha):
        '''
        Creates and returns an image pattern
        - (ox,oy) specify the top-left location of the image pattern
        - (ex,ey) specify the size of one image
        - angle, rotation around the top-left corner
        - image is the handle of the image to render
        The gradient is transformed by the current transform when it is passed to fillPaint() or strokePaint().
        '''
        return nvg.nvgImagePattern(self.ctx, ox, oy, ex, ey, angle, image, alpha)

    #####################################################
    # Scissoring
    # Scissoring allows you to clip the rendering into a rectangle
    # Useful for various user interface cases like rendering text edit or a timeline
    #
    #####################################################
    def scissor(self, float x, float y, float w, float h):
        '''
        Sets the current scissor rectangle
        The scissor rectangle is transformed by the current transform
        '''
        nvg.nvgScissor(self.ctx, x, y, w, h)

    def intersectScissor(self, float x, float y, float w, float h):
        '''
        Intersects current scissor rectangle with the specified rectangle
        The scissor rectangle is transformed by the current transform.
        Note:
            In case the rotation of previous scissor rect differs from
            the current one, the intersection will be done between the specified
            rectangle and the previous scissor rectangle transformed in the current
            transform space. The resulting shape is always rectangle.
        '''
        nvg.nvgIntersectScissor(self.ctx, x, y, w, h)

    def resetScissor(self):
        '''
        reset and disable scissoring
        '''
        nvg.nvgResetScissor(self.ctx)


    #####################################################
    # Paths
    # Drawing a new shape starts with beginPath()
    # - beginPath() clears all the currently defined paths.
    # - define one or more paths and sub-paths which describe the shape
    # functions to draw common shapes like:
    # - rectangles
    # - circles
    # - step-by-step functions to define a path curve by curve
    #
    # NanoVG uses even-odd fill rule to draw the shapes
    # - Solid shapes should have counter clockwise winding
    # - Holes should have counter clockwise order
    # To specify winding of a path you can call
    # - pathWinding() - useful especially for the common shapes, which are drawn CCW.
    #
    # Path fill and stroke can be set:
    # - fill() to set fill with current fill style
    # - stroke() to set stroke with current stroke style
    #
    # The curve segments and sub-paths are transformed by the current transform.
    # Drawing a new shape starts with nvgBeginPath(), it clears all the currently defined paths.
    #
    # The curve segments and sub-paths are transformed by the current transform.
    #####################################################
    def beginPath(self):
        '''
        clears the current path and sub-paths
        '''
        nvg.nvgBeginPath(self.ctx)

    def moveTo(self, float x, float y):
        '''
        starts the new sub-path with specified point as first point
        '''
        nvg.nvgMoveTo(self.ctx, x, y)

    def lineTo(self, float x, float y):
        '''
        adds line segment from the last point in the path to the specified point (pen analogy)
        '''
        nvg.nvgLineTo(self.ctx, x, y)

    def bezierTo(self, float c1x, float c1y, float c2x, float c2y, float x, float y):
        '''
        adds cubic bezier segment from last point in the path
        via two control points (c1, c2)
        to specified point (x,y)
        '''
        nvg.nvgBezierTo(self.ctx, c1x, c1y, c2x, c2y, x, y)

    def quadTo(self, float cx, float cy, float x, float y):
        '''
        adds a quadratic bezier segment from the last point in the path
        via one control point (cx, cy)
        to specified point (x, y)
        '''
        nvg.nvgQuadTo(self.ctx, cx, cy, x, y)

    def arcTo(self, float x1, float y1, float x2, float y2, float radius):
        '''
        adds an arc segment at the corner defined by the last path point and
        - two specified points (x1, y1) (x2,y2)
        - radius of arc
        '''
        nvg.nvgArcTo(self.ctx, x1, y1, x2, y2, radius)

    def closePath(self):
        '''
        close current sub-path with a line segment
        '''
        nvg.nvgClosePath(self.ctx)

    def pathWinding(self, int d):
        '''
        sets current sub-path winding with NVGwinding enum (d)
        - NVG_CCW    = 1
        - NVG_CW     = 2
        '''
        nvg.nvgPathWinding(self.ctx, d)

    def arc(self, float cx, float cy, float r, float a0, float a1, int d):
        '''
        creates new circle arc shaped sub-path
        - arc center is at point (cx,cy)
        - arc radius is r
        - drawn from angle a0 to angle a1
        - sweep direction (d) -- (NVG_CCW = 1, or NVG_CW = 2)
        angles specified in radians
        '''
        nvg.nvgArc(self.ctx, cx, cy, r, a0, a1, d)

    def rect(self, float x, float y, float w, float h):
        '''
        creates a new rectangle shaped sub-path from
        - top left (x,y)
        - width, height
        '''
        nvg.nvgRect(self.ctx, x, y, w, h)

    def roundedRect(self, float x, float y, float w, float h, float r):
        '''
        creates a rounded rectangle sub-path from
        - top left (x,y)
        - width, height
        - r rounding radius in radians
        '''
        nvg.nvgRoundedRect(self.ctx, x, y, w, h, r)

    def ellipse(self, float cx, float cy, float rx, float ry):
        '''
        creates a new ellipse shaped sub-path from
        - center point (cx,cy)
        - radius X (rx)
        - radius Y (ry)
        '''
        nvg.nvgEllipse(self.ctx, cx, cy, rx, ry)

    def circle(self, float cx, float cy, float r):
        '''
        creates a new circle shaped sub-path from
        - center point (cx, cy)
        - radius (r)
        '''
        nvg.nvgCircle(self.ctx, cx, cy, r)

    def fill(self):
        '''
        fills the current path with the current fill style
        '''
        nvg.nvgFill(self.ctx)

    def stroke(self):
        '''
        sets the current path with the current stroke style
        '''
        nvg.nvgStroke(self.ctx)

    #####################################################
    # Text
    # NanoVG allows you to load .ttf files and use the font to render text
    # The appearance of the text can be defined by setting the current text style
    # and by specifying the fill color.
    # Common text and font settings are supported:
    # - font size
    # - letter spacing
    # - text align
    #
    # Font blur allows you to create simple text effects such as drop shadows
    #
    # At render time the font face can be set based on the font handles or name.
    #
    # Font measure functions return values in local space, the calculations are
    # carried in the same resolution as the final rendering.
    # This is done because the text glyph positions are snapped to the nearest pixels sharp rendering.
    #
    # The local space means that values are not rotated or scaled as per the current transformation.
    # For example if you set font size to 12, which would mean that line height is 16 -
    # then regardless of the current scaling and rotation, the returned line height is always 16.
    #
    # Some measures may vary because of the scaling since aforementioned pixel snapping.
    # While this may sound a little odd, the setup allows you to always render the same way regardless of scaling.
    # i.e. the following works regardless of scaling:
    #         txt = "Text me up."
    #         vg.textBounds(x,y, txt, NULL, bounds);
    #         vg.beginPath()
    #         vg.roundedRect(bounds[0],bounds[1], bounds[2]-bounds[0], bounds[3]-bounds[1])
    #         vg.fill()
    #
    # Note: only solid color fill is currently supported for text.
    #####################################################
    def createFont(self, const char* name, const char* filename):
        '''
        creates a font by loading from the disk from specified filename
        - name you want to call the font internally e.g. "font_name"
        - filename of font e.g "roboto.ttf"
        returns handle to the font
        '''
        return nvg.nvgCreateFont(self.ctx, name, filename)

    def createFontMem(self, const char* name, unsigned char* data, int ndata, int freeData):
        '''
        creates image by loading it from specified memory chunk
        returns handle to the font
        '''
        return nvg.nvgCreateFontMem(self.ctx, name, data, ndata, freeData)

    def findFont(self, const char* name):
        '''
        finds a loaded font by its name and returns a handle to it
        if not found returns -1
        '''
        return nvg.nvgFindFont(self.ctx, name)

    def fontSize(self, float size):
        '''
        sets the font size of the current text style
        '''
        nvg.nvgFontSize(self.ctx, size)

    def fontBlur(self, float blur):
        '''
        sets the blur of the current text style
        '''
        nvg.nvgFontBlur(self.ctx, blur)

    def textLetterSpacing(self, float spacing):
        '''
        sets the letter spacing of the current text style
        '''
        nvg.nvgTextLetterSpacing(self.ctx, spacing)

    def textLineHeight(self, float lineHeight):
        '''
        sets the proportional line height of the current text style
        the line height is specified as a multiple of the font size
        '''
        nvg.nvgTextLineHeight(self.ctx, lineHeight)

    def textAlign(self, int align):
        '''
        sets the text alignment of the current text style
        Horizontal align
            - NVG_ALIGN_LEFT      = 1<<0  Default, align text horizontally to left.
            - NVG_ALIGN_CENTER    = 1<<1  Align text horizontally to center.
            - NVG_ALIGN_RIGHT     = 1<<2  Align text horizontally to right.
        Vertical align
            - NVG_ALIGN_TOP       = 1<<3  Align text vertically to top.
            - NVG_ALIGN_MIDDLE    = 1<<4  Align text vertically to middle.
            - NVG_ALIGN_BOTTOM    = 1<<5  Align text vertically to bottom.
            - NVG_ALIGN_BASELINE  = 1<<6  Default, align text vertically to baseline.
        '''
        nvg.nvgTextAlign(self.ctx, align)

    def fontFaceId(self, int font):
        '''
        sets the font face based on the specified id of the current text style
        '''
        nvg.nvgFontFaceId(self.ctx, font)

    def fontFace(self, const char* font):
        '''
        sets the font face based on the specified name of the current text style
        '''
        nvg.nvgFontFace(self.ctx, font)

    def text(self, float x, float y, const char* txt, const char* end=NULL):
        '''
        draws text string (txt) at specified location
        if end is specified, only the sun-string up to the end is drawn
        '''
        return nvg.nvgText(self.ctx, x, y, txt, end)

    def textBox(self, float x, float y, float breakRowWidth, const char* txt, const char* end):
        '''
        draws multi-line text string (txt) at specified location (x,y) wrapped at the specified width.
        If end is specified only the sub-string up to the end is drawn.
        White space is stripped at the beginning of the rows
        the text is split at word boundaries or when new-line characters are encountered
        Words longer than the max width are split at nearest character (i.e. no hyphenation)
        '''
        nvg.nvgTextBox(self.ctx, x, y, breakRowWidth, txt, end)

    def textBounds(self, float x, float y, const char* txt, const char* end=NULL):
        '''
        Measures the specified multi-text string.
        - (bounds) should be a pointer to float[4], if the bounding box of the text should be returned.
        The bounds value are [xmin,ymin, xmax,ymax]
        Measured values are returned in local coordinate space.
        '''
        cdef float bounds[4]
        length = nvg.nvgTextBounds(self.ctx, x, y, txt, end, bounds)
        return length,bounds[0],bounds[1],bounds[2],bounds[3]

    # def textGlyphPositions(self, float x, float y, const char* txt, const char* end=NULL, int ma0itions=0):
    #     '''
    #     Calculates the glyph x positions of the specified text.
    #     If end is specified only the sub-string will be used.
    #     Measured values are returned in local coordinate space.
    #     '''
    #     cdef nvg.NVGglyphPosition* pos
    #     retval = nvg.nvgTextGlyphPositions(self.ctx, x, y, txt, end, pos, ma0itions)
    #     return retval #,pos.x,pos.minx,pos.maxx

    def textMetrics(self, ascender=None,descender=None,lineh=None):
        '''
        Returns the vertical metrics based on the current text style.
        Measured values are returned in local coordinate space.

        it works but what does it do? how is this supposed to be used?
        '''
        cdef float asc[1]
        cdef float dsc[1]
        cdef float lh[1]
        if ascender: asc[0]=ascender
        if descender: dsc[0]=descender
        if lineh: lh[0]=lineh
        nvg.nvgTextMetrics(self.ctx, asc,dsc,lh)
        if ascender: return asc[0]
        if descender: return dsc[0]
        if lineh: return lh[0]


    def textBreakLines(self, const char* txt, const char* end=NULL, float breakRowWidth=0, int maxRows=0):
        '''
        Breaks the specified text (txt) into lines.
        If end is specified only the sub-string will be used.
        White space is stripped at the beginning of the rows
        the text is split at word boundaries or when new-line characters are encountered.
        Words longer than the max width are split at nearest character (i.e. no hyphenation).
        '''
        cdef const char* c_end = NULL
        cdef nvg.NVGtextRow* r = NULL
        return <int>nvg.nvgTextBreakLines(self.ctx, txt, c_end, breakRowWidth, r, maxRows)

    ### Wrapper functions
    # below are functions that exsist to make drawing many things possible in Python

    @cython.boundscheck(False) # turn off bounds-checking for entire function
    def Circles(self,np.ndarray[DTYPE_t, ndim=2] positions,float r=10):
        cdef Py_ssize_t n_points = positions.shape[0]
        cdef Py_ssize_t n
        if positions.shape[1] == 2:
            for n in range(n_points):
                nvg.nvgCircle(self.ctx, positions[n,0], positions[n,1], r)
        else:
            for n in range(n_points):
                nvg.nvgCircle(self.ctx, positions[n,0], positions[n,1], positions[n,2])

    @cython.boundscheck(False) # turn off bounds-checking for entire function
    def Polyline(self, np.ndarray[DTYPE_t, ndim=2] polyline,float sw=1):
        cdef Py_ssize_t n_segments = polyline.shape[0]
        cdef Py_ssize_t n
        self.strokeWidth(sw)
        nvg.nvgBeginPath(self.ctx)
        nvg.nvgMoveTo(self.ctx,polyline[0,0],polyline[0,1])
        for n in range(1,n_segments):
            nvg.nvgLineTo(self.ctx,polyline[n,0],polyline[n,1])

    @cython.boundscheck(False) # turn off bounds-checking for entire function
    def Polylines(self, np.ndarray[DTYPE_t, ndim=3] polyline,float sw=1):
        cdef Py_ssize_t n_lines = polyline.shape[0]
        cdef Py_ssize_t n_segments = polyline.shape[1]
        cdef Py_ssize_t l,s
        self.strokeWidth(sw)
        for l in range(n_lines):
            nvg.nvgBeginPath(self.ctx)
            nvg.nvgMoveTo(self.ctx,polyline[l,0,0],polyline[l,0,1])
            for s in range(1,n_segments):
                nvg.nvgLineTo(self.ctx,polyline[l,s,0],polyline[l,s,1])
