import sys
from pygf.tikz import TikzLayer
from pygf.svg import SvgLayer
from pygf.geometry import Point, Rectangle
import math
from common import *

arrows = [">-<", "<->", "latex-xetal", "x-x", "xetal-latex"]

def sanitize(name):
    if tex:
        return rf"\texttt{{{name}}}"
    else:
        return name
    
for i in range(len(arrows)):
    layer.line(Point(0, 5-i), Point(5, 5-i + 0.5), arrow=arrows[i])
    layer.text(Point(-5, 5-i), sanitize(f"arrow={arrows[i]}"), position="right")


layer.draw(Rectangle(Point(-6, 0), Point(6, 6)), open(fn, "w"), preamble=True)
