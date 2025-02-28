import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform,Point, Rectangle
import math

layer1,layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])


layer.polyline([Point(0,0), Point(2,3) , Point(4,3), Point(6,0)],
                labels= {
                    "above start": "above start" ,
                    "above": "above", 
                    "above end": "above end" ,
                    "below start": "below start" ,
                    "below": "below", 
                    "below end": "below end" }
               )


layer.edge([Point(-6,0), Point(-4,3) , Point(-2,3), Point(0,0)],
                labels= {
                    "above start": "above start" ,
                    "above": "above", 
                    "above end": "above end" ,
                    "below start": "below start" ,
                    "below": "below", 
                    "below end": "below end" }
               )


layer.draw(Rectangle(Point(-7,-1), Point(7,5)), [open("poly.tex", "w"), open("poly.svg", "w")], preamble=True)


