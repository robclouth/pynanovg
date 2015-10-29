import glfw
import OpenGL
from OpenGL.GL import *
import time

class Base(object):
    def __init__(self, width, height):
        self.quit = False
        self.width = width
        self.height = height

    def on_resize(self, window, w, h):
        active_window = glfw.get_current_context()
        glfw.make_context_current(window)
        # norm_size = normalize((w,h),glfwGetWindowSize(window))
        # fb_size = denormalize(norm_size,glfwGetFramebufferSize(window))
        self.adjust_gl_view(w, h, window)
        glfw.make_context_current(active_window)
        self.width, self.height = w, h

    def on_key(self, window, key, scancode, action, mods):
        # print "key pressed: ", key
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                on_close(window)

    def on_button(self, window, button, action, mods):
        pos = glfw.get_cursor_pos(window)
        # pos = normalize(pos,glfwGetWindowSize(window))
        # pos = denormalize(pos,(frame.img.shape[1],frame.img.shape[0]) ) # Position in img pixels

    def on_close(self, window):
        self.quit = True

    def basic_gl_setup(self):
        glEnable(GL_POINT_SPRITE)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE) # overwrite pointsize
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glClearColor(0., 0., 0., 1.0)

    def adjust_gl_view(self, w, h, window):
        """
        adjust view onto our scene.
        """
        h = max(h, 1)
        w = max(w, 1)

        hdpi_factor = glfwGetFramebufferSize(window)[0]/glfwGetWindowSize(window)[0]
        w,h = w*hdpi_factor,h*hdpi_factor
        glViewport(0, 0, w, h)

    def clear_screen(self):
        glClearColor(0.7, 0.7, 0.7, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT)

    def setup(self):
        # get glfw started
        glfw.init()
        self.window = glfw.create_window(self.width, self.height, "Python NanoVG Demo", None, None)
        glfw.set_window_pos(self.window, 0, 0)

        # Register callbacks window
        glfw.set_window_size_callback(self.window, self.on_resize)
        glfw.set_window_close_callback(self.window, self.on_close)
        glfw.set_key_callback(self.window, self.on_key)
        glfw.set_mouse_button_callback(self.window, self.on_button)

        self.basic_gl_setup()

        # glfwSwapInterval(0)
        glfw.make_context_current(self.window)

    def update(self):
        self.mouse = glfw.get_cursor_pos(self.window)

    def run(self):
        self.setup()
        while not self.quit:
            self.clear_screen()
            self.update()
            self.render()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            # time.sleep(.03)
        self.teardown()

    def teardown(self):
        glfw.destroy_window(self.window)
        glfw.terminate()


