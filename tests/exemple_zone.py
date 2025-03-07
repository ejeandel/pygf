import sys
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform,Point, Rectangle
import argparse    
parser = argparse.ArgumentParser(description='')
parser.add_argument('--tex', dest='tex', action="store_true", help='tex or svg output')



args = parser.parse_args()

if args.tex:
    layer = TikzLayer()
    fn = "exemple_zone.tex"
else:
    layer = SvgLayer()
    fn = "exemple_zone.svg"


layer.circle(Point(-3,0),4, fill="Pink", z_index=-1)
layer.circle(Point(3,3),2.5, fill="Thistle", z_index=-1)
layer.circle(Point(3,-3),2.5, fill="GreenYellow", z_index=-1)
layer.circle(Point(9,0),4, fill="LightGray", z_index=-1)
    
A = Point(0,0)
B = Point(2,1)
C = Point(4,1)
D = Point(3,-1)
E = Point(6,0)  
F = Point(-4,0)
G = Point(9,0)

for i in A,B,C,D,E:
    layer.picture(i, "router.png", width=1, height=0.7)
    
layer.text(A + Point(0,0.5), "A", position="above")
layer.text(B + Point(0,0.5), "B", position="above")
layer.text(C + Point(0,0.5), "C", position="above")
layer.text(D + Point(0,0.5), "D", position="above")
layer.text(E + Point(0,0.5), "E", position="above")
layer.line(A,B)
layer.line(B,C)
layer.line(C,E)
layer.line(E,D)
layer.line(D,A)
layer.line(A,F, labels={"above": "140.77.128.0/24"})
layer.line(E,G, labels={"above": "12.10.4.0/24"})


layer.draw(Rectangle(Point(-5,2), Point(10,-2)), open(fn, "w"), preamble=True)
