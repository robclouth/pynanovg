PyNanoVG
========

... work in progress ...

[Cython](https://github.com/cython/cython) powered bindings for [NanoVG](https://github.com/memononen/nanovg)

Dependencies
============

+ Cython

Build NanoVG
============

    $ python3 setup.py build_ext -i

Builds 'pynanovg.nanovg' package 'pynanovg/nanovg.so' using cython files from ./ and nanovg sourcefiles from nanovg submodule.
This module does not use the nanovg lua toolchain and instead builds nanovg from source. See setup.py.

So far we only build the nanovg.so file which can be locally imported using python.

Usage
=====

- Make sure you have a python binding to GLFW3 installed

    $ cp ./build/lib.<system>/pynanovg/nanovg.so ./examples/pynanovg/
    $ cd ./examples
    $ python3 demo.py
