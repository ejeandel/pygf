from pygf.geometry import Point, Rectangle
from pygf.layer import MultiLayer
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

thick = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4]

for i in range(len(thick)):
    layer.line(Point(0, i), Point(1, i), thickness=thick[i])
    layer.text(Point(-3, i), f"thickness = {thick[i]}")

with open("thickness.tex", "w") as f1, open("thickness.svg", "w") as f2:
    layer.draw_all(Rectangle(Point(-6, -1), Point(6, 10)), [f1, f2], preamble=True)
