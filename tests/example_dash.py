import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform,Point, Rectangle
import math

layer1,layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])

dash =     ["solid","dotted","densely dotted","loosely dotted","dashed","densely dashed","loosely dashed","dashdotted","dash dot","densely dashdotted","densely dash dot","loosely dashdotted","loosely dash dot","dashdotdotted","densely dashdotdotted", "loosely dashdotdotted","dash dot dot","densely dash dot dot","loosely dash dot dot"]

for i in range(len(dash)):
    layer.line(Point(0,i), Point(5,i), dash = dash[i])
    layer.text(Point(-3,i), f"dash = {dash[i]}")

layer.draw(Rectangle(Point(-6,-1), Point(6,20)), [open("dash.tex", "w"), open("dash.svg", "w")], preamble=True)


