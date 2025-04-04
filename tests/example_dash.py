from pygf.geometry import Point, Rectangle
from pygf.layer import MultiLayer
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

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
    layer.line(Point(0, i), Point(5, i), dash=dash[i])
    layer.text(Point(-3, i), f"dash = {dash[i]}")

with open("dash.tex", "w") as f1, open("dash.svg", "w") as f2:
    layer.draw_all(Rectangle(Point(-6, -1), Point(6, 20)), [f1, f2], preamble=True)
