import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform, Point, Rectangle
import math

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])


layer.polyline([Point(0, 0), Point(2, 3), Point(4, 3), Point(6, 0)], rounded=True)

layer.polyline([Point(0, 4), Point(2, 7), Point(4, 7), Point(6, 4)], rounded=True, closed=True)


layer.draw_all(
    Rectangle(Point(-8, -1), Point(7, 8)),
    [open("poly2.tex", "w"), open("poly2.svg", "w")],
    preamble=True,
)
