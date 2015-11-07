import sys, os, platform
from codecs import open

from setuptools import setup

OPENGL_VERSION='gl3'

for arg in iter(sys.argv):
    if arg.startswith('--opengl='):
        _, version = arg.split('=', 1)
        sys.argv.remove(arg)

try:
    import numpy
except ImportError:
    print('Please install numpy.')
    exit(1)

try:
    import Cython
except ImportError:
    print('Please install Cython.')
    exit(1)

###############################################################################
name = 'pynanovg'
description = 'NanoVG Python Bindings'

author = "Hector Dearman"
author_email = "hector.dearman@gmail.com"
license = "MIT"
version = '0.0.2'

setup_requires = [
    'numpy',
    'Cython',
],
install_requires = [
    'numpy',
]
tests_require = [
    'pytest',
]
dev_requires = tests_require + [
    'tox',
    'check-manifest',
]
extras_require = {
    'test': tests_require,
    'dev': dev_requires,
}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

###############################################################################

include_dirs = []

if platform.system() == 'Darwin':
    import numpy
    include_dirs = ['OpenGL/gl.h', numpy.get_include()]
    libs = []
    link_args = ['-framework', 'OpenGL']
else:
    include_dirs = ['/usr/include/GL']
    libs = ['GL', 'GLU', 'GLEW', 'm']
    link_args = []

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
        implementation = {
                'gl2': 'NANOVG_GL2_IMPLEMENTATION',
                'gl3': 'NANOVG_GL3_IMPLEMENTATION',
                'gles2': 'NANOVG_GLES2_IMPLEMENTATION',
                'gles3': 'NANOVG_GLES3_IMPLEMENTATION',
        }[OPENGL_VERSION]
        m.extra_compile_args = ['-D ' + implementation]

    return cython_modules

setup(
    name = name,
    description = description,
    long_description = long_description,
    author = author,
    author_email = author_email,
    license = license,
    version = version,

    setup_requires = setup_requires,
    install_requires = install_requires,
    tests_require = tests_require,
    extras_require = extras_require,

    packages = [
        'pynanovg',
    ],

    ext_modules = ext_modules(),
    include_dirs = include_dirs,
)
