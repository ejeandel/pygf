from pygf.geometry import Point, Rectangle
from pygf.layer import MultiLayer
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])


layer.polyline([Point(0, 0), Point(2, 3), Point(4, 3), Point(6, 0)], rounded=True)

layer.polyline([Point(0, 4), Point(2, 7), Point(4, 7), Point(6, 4)], rounded=True, closed=True)


with open("poly2.tex", "w") as f1, open("poly2.svg", "w") as f2:
    layer.draw_all(Rectangle(Point(-8, -1), Point(7, 8)), [f1, f2], preamble=True)
