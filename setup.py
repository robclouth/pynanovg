import os, platform
import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

if platform.system() == 'Darwin':
    includes = ['OpenGL/gl.h', numpy.get_include()]
    link_args = ['-framework', 'OpenGL'] 
    libs = []
else:
    includes = ['/usr/include/GL']
    libs = ['GL', 'GLU', 'GLEW', 'm']
    link_args = []

extensions = [
    Extension(  name = 'pynanovg.pynanovg',
                sources = ['src/pynanovg.pyx', 'nanovg/src/nanovg.c'],
                include_dirs = includes + ['nanovg/src'], 
                libraries = libs,
                extra_link_args = link_args,

                # gl2 backend is hardcoded
                # TODO: enable use of any of the following: 
                #     NANOVG_GL2_IMPLEMENTATION, NANOVG_GL3_IMPLEMENTATION, 
                #     NANOVG_GLES2_IMPLEMENTATION, NANOVG_GLES3_IMPLEMENTATION
                extra_compile_args = ['-D NANOVG_GL2_IMPLEMENTATION'] ),
]

setup(  name = 'pynanovg',
        version = '0.0.2',
        description = 'NanoVG Python Bindings',
        ext_modules = cythonize(extensions)
)