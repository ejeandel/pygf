from pygf.geometry import Point, Rectangle
from pygf.layer import MultiLayer
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

arrows = [">-<", "<->", "latex-xetal", "x-x", "xetal-latex"]

layer.line(Point(5, 0), Point(5, 10), draw="red")
layer.line(Point(0, -1), Point(0, 10), draw="red")

for i in range(len(arrows)):
    layer.line(Point(0, i), Point(5, i + 0.5), arrow=arrows[i])
    layer.text(Point(-3, i), f"arrow = {arrows[i]}")


with open("arrows.tex", "w") as f1, open("arrows.svg", "w") as f2:
    layer.draw_all(Rectangle(Point(-6, -1), Point(6, 20)), [f1, f2], preamble=True)
