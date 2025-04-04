import sys

from pygf.geometry import Point as p
from pygf.geometry import Rectangle
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

""" choose if you want to you Svg or Tikz to render the picture """
tikz = False

layer = TikzLayer() if tikz else SvgLayer()


""" add a point """

layer.text(p(0, 0), "A", position="above")

""" add a line """
layer.line(p(0, 0), p(5, -5), arrow="->", labels={"above end": "line with text at the end"})

""" add an edge. An edge is a curve that connect multiple points (at least 2).
You need to specify at which angle the curve should leave through the point.
"""

layer.edge([p(0, 0) @ {"angle": 180}, p(0, -2) @ {"angle": 0}, p(2, -2) @ {"angle": 60}], draw="Red")

layer.edge([p(0, 0), p(0, -2), p(2, -2)], draw="Blue")

layer.edge([p(0, -3), p(0, -5), p(2, -5)], draw="Blue", fill="Red")


""" draw a circle and a rectangle """

layer.circle(p(4, -2), 1, fill="Red")

layer.rectangle(p(4, -2), p(1, -4), fill="Blue")


""" draw the result. You need to specify the bounding box you want """

if tikz:
    with open("test.tex", "w") as f:
        layer.draw(Rectangle(p(-2, -10), p(10, 2)), f, preamble=True)
else:
    with open("test.svg", "w") as f:
        layer.draw(Rectangle(p(-2, -10), p(10, 2)), f, preamble=True)


sys.exit(0)
