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


layer.polyline([Point(0,4), Point(2,7) , Point(4,7), Point(6,4)][::-1],
                labels= {
                    "above start": "above start" ,
                    "above": "above",
                    "above end": "above end" ,
                    "below start": "below start" ,
                    "below": "below",
                    "below end": "below end" }
               )


layer.edge([Point(-7,0), Point(-5,3) , Point(-3,3), Point(-1,0)],
                labels= {
                    "above start": "above start" ,
                    "above": "above",
                    "above end": "above end" ,
                    "below start": "below start" ,
                    "below": "below",
                    "below end": "below end" }
               )


layer.edge([Point(-7,4), Point(-5,7) , Point(-3,7), Point(-1,4)][::-1],
                labels= {
                    "above start": "above start" ,
                    "above": "above", 
                    "above end": "above end" ,
                    "below start": "below start" ,
                    "below": "below", 
                    "below end": "below end" }
               )


layer.draw(Rectangle(Point(-8,-1), Point(7,8)), [open("poly.tex", "w"), open("poly.svg", "w")], preamble=True)


