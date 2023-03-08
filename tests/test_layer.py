import sys
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Layer import Wire,Node
from pygf.Geometry import Transform,Point, Rectangle
import math

tf = Transform(x=1,y=1)
layer = SvgLayer(tf)
#layer = TikzLayer(tf)


layer.text(Point(0,0),"A", position="above")
layer.text(Point(6,0),"B", position="above")

layer.line(Point(0,0), Point(0,-5.5))
layer.line(Point(6,0), Point(6,-5.5))



layer.line(Point(0.5,0),Point(5.5,-1),
           style = {"arrow": "->"},
           labels = {
               "above end" : "octets 0...499"
           })

layer.line(Point(5.5,-1.5), Point(0.5,-2.5),
           style = {"arrow": "->"},
           labels = {
               "above end" : "ACK"
           }
)


layer.edge([(Point(0,0), 60), (Point(1, 0.5), 180)])

x1 = 0
x2 = 1

# on part en 0, 0


"""  lineto(-x1    , .5amplitude)
    curveto
      (-.5x1, .5amplitude)
      (-.15x1, .3amplitude)

    {
      \pgftransformxshift{+\pgfdecorationsegmentaspect\pgfdecoratedremainingdistance}
      \pgfpathlineto{\pgfqpoint{-x1}{.5\amplitude}}
      \pgfpathcurveto
      {\pgfqpoint{-.5x1}{.5\amplitude}}
      {\pgfqpoint{-.15x1}{.7\amplitude}}
      {\pgfqpoint{0x1}{1\amplitude}}
      \pgfpathcurveto
      {\pgfqpoint{.15x2}{.7\amplitude}}
      {\pgfqpoint{.5x2}{.5\amplitude}}
      {\pgfqpoint{x2}{.5\amplitude}}
    }
    {
      \pgftransformxshift{+\pgfdecoratedremainingdistance}
      \pgfpathlineto{\pgfqpoint{-x2}{.5\amplitude}}
      \pgfpathcurveto
      {\pgfqpoint{-.5x2}{.5\amplitude}}
      {\pgfqpoint{-.15x2}{.3\amplitude}}
      {\pgfqpoint{0pt}{0pt}}
    }
  }%
"""

#layer.edge([(Point(0,0),45), (Point(6, -2), 45), (Point(6,-1),180)], labels = {
#    "above end" : "..........ACK........."
#}
#)



#\draw[->,font=\scriptsize] (0.5,0) -- (5.5,-1)  node [sloped,pos=0, above right]{octets 0..499}; 
#\draw[->,font=\scriptsize] (5.5,-1.5) -- (0.5,-2.5)  node [sloped,pos=0, above left]{ACK}; 
#\draw[->,font=\scriptsize] (0.5,-3.0) -- (5.5,-4.0)  node [sloped,pos=0, above right]{octets 500..999}; 
#\draw[->,font=\scriptsize] (5.5,-4.5) -- (0.5,-5.5)  node [sloped,pos=0, above left]{ACK}; 


#layer.rectangle(Point(0,0), Point(2,1))
#layer.rectangle(Point(2,1), Point(3,5))
layer.draw(Rectangle(Point(-2,-10), Point(10,2)), open("test.svg", "w"), preamble=True)


sys.exit(0)


n1 = Node(Point(1,2), {'label':'qsfklj', 'shape': 'circle', 'draw':'', 'invariant': False})
n2 = Node(Point(2,3), {'label':'qsfklj', 'shape': 'circle', 'draw':''})
n3 = Node(Point(3,4), {'shape': 'circle', 'draw':''})
n4 = Node(Point(4,6), {'shape': 'circle', 'draw':''})

layer.new_node(n1)
layer.new_node(n2)
layer.new_node(n3)
layer.new_node(n4)

w = Wire(n1, 0, {'draw': 'black'})
w.add(n2, None)
w.add(n3, None)
w.add(n4, 0)
layer.new_edge(w)


w = Wire(n1, None, {'draw': 'black'})
w.add(n2, None)
layer.new_edge(w)



