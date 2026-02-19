import sys
from pygf.tikz import TikzLayer
from pygf.svg import SvgLayer
from pygf.geometry import Point, Rectangle
import math
from common import *




dash = [
    "solid",
    "dotted",
    "densely dotted",
    "loosely dotted",
    "dashed",
    "densely dashed",
    "loosely dashed",
    "dashdotted",
    "dash dot",
    "densely dashdotted",
    "densely dash dot",
    "loosely dashdotted",
    "loosely dash dot",
    "dashdotdotted",
    "densely dashdotdotted",
    "loosely dashdotdotted",
    "dash dot dot",
    "densely dash dot dot",
    "loosely dash dot dot",
]

for i in range(len(dash)):
    layer.line(Point(0, 18-i), Point(5, 18-i), dash=dash[i])
    layer.text(Point(-5, 18-i), f'dash="{dash[i]}"', position="right")

layer.draw(Rectangle(Point(-6, -0.5), Point(6, 18.5)), open(fn, "w"), preamble=True)
