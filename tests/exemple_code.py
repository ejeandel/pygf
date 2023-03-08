import sys
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Transform,Point, Rectangle
import math

import argparse    
parser = argparse.ArgumentParser(description='')
parser.add_argument('--tex', dest='tex', action="store_true", help='tex or svg output')

args = parser.parse_args()

if args.tex:
    layer = TikzLayer()
    fn = "code5.tex"
else:
    layer = SvgLayer()
    fn = "code5.svg"

x00000= Point(5.2,0*math.pi/180,polar=True) , "00000"
x00001= Point(4.2,0*math.pi/180,polar=True) , "00001"
x00110= Point(3,0*math.pi/180,polar=True) , "00110"
x00111= Point(1.8,0*math.pi/180,polar=True) , "00111"
x00010= Point(5.2,45*math.pi/180,polar=True) , "00010"
x00011= Point(4.2,45*math.pi/180,polar=True) , "00011"
x01000= Point(3,45*math.pi/180,polar=True) , "01000"
x01001= Point(1.8,45*math.pi/180,polar=True) , "01001"
x00100= Point(5.2,-45*math.pi/180,polar=True) , "00100"
x00101= Point(4.2,-45*math.pi/180,polar=True) , "00101"
x10000= Point(3,-45*math.pi/180,polar=True) , "10000"
x10001= Point(1.8,-45*math.pi/180,polar=True) , "10001"

x01010= Point(5.2,90*math.pi/180,polar=True) , "01010"
x01011= Point(4.2,90*math.pi/180,polar=True) , "01011"
x10010= Point(3,90*math.pi/180,polar=True) , "10010"
x10011= Point(1.8,90*math.pi/180,polar=True) , "10011"

x11010= Point(5.2,135*math.pi/180,polar=True) , "11010"
x11011= Point(4.2,135*math.pi/180,polar=True) , "11011"
x01110= Point(3,135*math.pi/180,polar=True) , "01110"
x01111= Point(1.8,135*math.pi/180,polar=True) , "01111"

x11110= Point(5.2,180*math.pi/180,polar=True) , "11110"
x11111= Point(4.2,180*math.pi/180,polar=True) , "11111"


x10100= Point(5.2,-90*math.pi/180,polar=True) , "10100"
x10101= Point(4.2,-90*math.pi/180,polar=True) , "10101"
x01100= Point(3,-90*math.pi/180,polar=True) , "01100"
x01101= Point(1.8,-90*math.pi/180,polar=True) , "01101"

x11100= Point(5.2,-135*math.pi/180,polar=True) , "11100"
x11101= Point(4.2,-135*math.pi/180,polar=True) , "11101"
x10110= Point(3,-135*math.pi/180,polar=True) , "10110"

x11000= Point(3,180*math.pi/180,polar=True) , "11000"

x10111= Point(1.8,-135*math.pi/180,polar=True) , "10111"
x11001= Point(1.8,180*math.pi/180,polar=True) , "11001"



layer.line(x00000[0],x10000[0])
layer.line(x00000[0],x01000[0])
layer.line(x00000[0],x00100[0])
layer.line(x00000[0],x00010[0])
layer.line(x00000[0],x00001[0])
layer.line(x00001[0],x10001[0])
layer.line(x00001[0],x01001[0])
layer.line(x00001[0],x00101[0])
layer.line(x00001[0],x00011[0])
layer.line(x00010[0],x10010[0])
layer.line(x00010[0],x01010[0])
layer.line(x00010[0],x00110[0])
layer.line(x00010[0],x00011[0])
layer.line(x00011[0],x10011[0])
layer.line(x00011[0],x01011[0])
layer.line(x00011[0],x00111[0])
layer.line(x00100[0],x10100[0])
layer.line(x00100[0],x01100[0])
layer.line(x00100[0],x00110[0])
layer.line(x00100[0],x00101[0])
layer.line(x00101[0],x10101[0])
layer.line(x00101[0],x01101[0])
layer.line(x00101[0],x00111[0])
layer.line(x00110[0],x10110[0])
layer.line(x00110[0],x01110[0])
layer.line(x00110[0],x00111[0])
layer.line(x00111[0],x10111[0])
layer.line(x00111[0],x01111[0])
layer.line(x01000[0],x11000[0])
layer.line(x01000[0],x01100[0])
layer.line(x01000[0],x01010[0])
layer.line(x01000[0],x01001[0])
layer.line(x01001[0],x11001[0])
layer.line(x01001[0],x01101[0])
layer.line(x01001[0],x01011[0])
layer.line(x01010[0],x11010[0])
layer.line(x01010[0],x01110[0])
layer.line(x01010[0],x01011[0])
layer.line(x01011[0],x11011[0])
layer.line(x01011[0],x01111[0])
layer.line(x01100[0],x11100[0])
layer.line(x01100[0],x01110[0])
layer.line(x01100[0],x01101[0])
layer.line(x01101[0],x11101[0])
layer.line(x01101[0],x01111[0])
layer.line(x01110[0],x11110[0])
layer.line(x01110[0],x01111[0])
layer.line(x01111[0],x11111[0])
layer.line(x10000[0],x11000[0])
layer.line(x10000[0],x10100[0])
layer.line(x10000[0],x10010[0])
layer.line(x10000[0],x10001[0])
layer.line(x10001[0],x11001[0])
layer.line(x10001[0],x10101[0])
layer.line(x10001[0],x10011[0])
layer.line(x10010[0],x11010[0])
layer.line(x10010[0],x10110[0])
layer.line(x10010[0],x10011[0])
layer.line(x10011[0],x11011[0])
layer.line(x10011[0],x10111[0])
layer.line(x10100[0],x11100[0])
layer.line(x10100[0],x10110[0])
layer.line(x10100[0],x10101[0])
layer.line(x10101[0],x11101[0])
layer.line(x10101[0],x10111[0])
layer.line(x10110[0],x11110[0])
layer.line(x10110[0],x10111[0])
layer.line(x10111[0],x11111[0])
layer.line(x11000[0],x11100[0])
layer.line(x11000[0],x11010[0])
layer.line(x11000[0],x11001[0])
layer.line(x11001[0],x11101[0])
layer.line(x11001[0],x11011[0])
layer.line(x11010[0],x11110[0])
layer.line(x11010[0],x11011[0])
layer.line(x11011[0],x11111[0])
layer.line(x11100[0],x11110[0])
layer.line(x11100[0],x11101[0])
layer.line(x11101[0],x11111[0])
layer.line(x11110[0],x11111[0])

    


    


for (a,b) in [x00000,x01000,x10000,x11000,x00100,x01100,x10100,x11100,x00010,x01010,x10010,x11010,x00110,x01110,x10110,x11110,
              x00001,x01001,x10001,x11001,x00101,x01101,x10101,x11101,x00011,x01011,x10011,x11011,x00111,x01111,x10111,x11111]:
    if b in ["11001", "11110","00111","00000"]:
        layer.circle(a,0.33, fill="Red")
    else:
        layer.circle(a,0.33, fill="White")        
    layer.text(a, b, text_size="small")

layer.draw(Rectangle(Point(-6,-6), Point(6,6)), open(fn, "w"), preamble=True)


