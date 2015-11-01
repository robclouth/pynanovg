PyNanoVG
========

... work in progress ...

[Cython](https://github.com/cython/cython) powered bindings for [NanoVG](https://github.com/memononen/nanovg)

Forked from [here](https://github.com/philetus/pynanovg).

Installation
------------
- `pip install Cython`
- `pip install numpy`
- `pip install pynanovg`

Use
---
```python
import pynanovg

# Set up an OpenGL window here

vg = pynanovg.Context()
vg.beginFrame()

vg.beginPath(vg)
vg.ellipse(100, 100, 10, 5)
vg.fillColor(0.1, 0.1, 0.9, 1.0)
vg.fill()

vg.endFrame()
```
