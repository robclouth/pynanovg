import os, platform
from codecs import open

import numpy

from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

from Cython.Build import cythonize

###############################################################################
name = 'pynanovg'
description = 'NanoVG Python Bindings'

author = "Hector Dearman"
author_email = "hector.dearman@gmail.com"
license = "MIT"
version = '0.0.2'

setup_requires = [
    'numpy',
],
install_requires = [
]
tests_require = [
    'pytest',
]
extras_require = {
    'test': tests_require,
}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

###############################################################################

if platform.system() == 'Darwin':
    include_dirs = ['OpenGL/gl.h', numpy.get_include()]
    libs = []
    link_args = ['-framework', 'OpenGL']
else:
    include_dirs = ['/usr/include/GL']
    libs = ['GL', 'GLU', 'GLEW', 'm']
    link_args = []

# Cython hack: http://stackoverflow.com/questions/11010151
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

# numpy hack: http://stackoverflow.com/questions/19919905/
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

setup(
    name = name,
    description = description,
    long_description = long_description,
    author = author,
    author_email = author_email,
    license = license,
    version = version,

    # numpy hack
    cmdclass={'build_ext':build_ext},

    setup_requires = setup_requires,
    install_requires = install_requires,
    tests_require = tests_require,
    extras_require = extras_require,

    packages = [
        'pynanovg',
    ],

    ext_modules = lazy_list(ext_modules),
)
