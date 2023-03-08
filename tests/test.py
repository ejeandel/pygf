import sys
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Layer import Wire,Node
from pygf.Geometry import Transform,Point, Rectangle
import math

""" choose if you want to you Svg or Tikz to render the picture """
tikz = False

if tikz:
    layer = TikzLayer()
else:
    layer = SvgLayer()


""" add a point """

layer.text(Point(0,0),"A", position="above")

""" add a line """
layer.line(Point(0,0), Point(5,-5), arrow="->", 
           labels = {
               "above end" : "line with text at the end"
           })

""" add an edge. An edge is a curve that connect multiple points (at least 2).
You need to specify at which angle the curve should leave through the point.
"""

layer.edge([(Point(0,0), 180), (Point(0, -2), 0), (Point(2,-2), 60)], draw="Red")

layer.edge([(Point(0,0), None), (Point(0, -2), None), (Point(2,-2), None)], draw = "Blue")

layer.edge([(Point(0,-3), None), (Point(0,-5), None), (Point(2,-5), None)], draw = "Blue", fill="Red")


""" draw a circle and a rectangle """

layer.circle(Point(4,-2),1,fill="Red")

layer.rectangle(Point(4,-2), Point(1,-4) ,fill="Blue")



""" draw the result. You need to specify the bounding box you want """

if tikz:
    layer.draw(Rectangle(Point(-2,-10), Point(10,2)), open("test.tex", "w"), preamble=True)
else:
    layer.draw(Rectangle(Point(-2,-10), Point(10,2)), open("test.svg", "w"), preamble=True)


sys.exit(0)

