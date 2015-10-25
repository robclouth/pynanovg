import os, platform
import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

include_dirs = []

if platform.system() == 'Darwin':
    include_dirs = ['OpenGL/gl.h', numpy.get_include()]
    libs = []
    link_args = ['-framework', 'OpenGL']
else:
    include_dirs = ['/usr/include/GL']
    libs = ['GL', 'GLU', 'GLEW', 'm']
    link_args = []

# Adapted from http://stackoverflow.com/questions/11010151
class lazy_list(list):
    def __init__(self, callback):
        self._list = None
        self.callback = callback

    @property
    def list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list

    def __iter__(self):
        for e in self.list:
            yield e

    def __getitem__(self, i):
        return self.list[i]

    def __len__(self):
        return len(self.list)

def ext_modules():
    from Cython.Build import cythonize
    cython_modules = cythonize('pynanovg/*.pyx')

    for m in cython_modules:
        m.libraries = libs
        m.extra_link_args = link_args

        # gl2 backend is hardcoded
        # TODO: enable use of any of the following: 
        # NANOVG_GL2_IMPLEMENTATION, NANOVG_GL3_IMPLEMENTATION, 
        # NANOVG_GLES2_IMPLEMENTATION, NANOVG_GLES3_IMPLEMENTATION
        m.extra_compile_args = ['-D NANOVG_GL2_IMPLEMENTATION']

    return cython_modules

setup(
    name = 'pynanovg',
    packages = [
        'pynanovg',
    ],
    license = "MIT",
    version = '0.0.2',
    description = 'NanoVG Python Bindings',
    ext_modules = lazy_list(ext_modules),
    include_dirs = include_dirs,
)
