import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform, Point, Rectangle
import math

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

thick = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4]

for i in range(len(thick)):
    layer.line(Point(0, i), Point(1, i), thickness=thick[i])
    layer.text(Point(-3, i), f"thickness = {thick[i]}")

layer.draw_all(
    Rectangle(Point(-6, -1), Point(6, 10)),
    [open("thickness.tex", "w"), open("thickness.svg", "w")],
    preamble=True,
)
