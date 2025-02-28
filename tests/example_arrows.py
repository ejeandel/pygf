import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform,Point, Rectangle
import math


layer1,layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

arrows =     [">-<", "<->", "latex-xetal", "x-x", "xetal-latex"]

layer.line(Point(5,0), Point(5,10), draw="red")
layer.line(Point(0,-1), Point(0,10), draw="red")

for i in range(len(arrows)):
    layer.line(Point(0,i), Point(5,i+.5), arrow = arrows[i])
    layer.text(Point(-3,i), f"arrow = {arrows[i]}")

    
layer.draw(Rectangle(Point(-6,-1), Point(6,20)), [open("arrows.tex", "w"), open("arrows.svg", "w")], preamble=True)


