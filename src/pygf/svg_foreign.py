"""Module that provides the SVG Layer"""

# pylint: disable=invalid-name
import base64
import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from pygf.svg import SvgLayer

from pygf.geometry import Point, Rectangle
class SvgForeignLayer(SvgLayer):
    """ Foreign SVG Layer"""

    def __init__(self, transform=None):
        SvgLayer.__init__(self, transform)
        self.namespaces['xhtml'] =  "http://www.w3.org/1999/xhtml"


    def text_input(self, p1, p2, text, z_index=1, **style):
        tf = self.svgtransform * self.transform
        
        r = Rectangle(tf(p1),tf(p2))
        foreign = ET.Element("foreignObject" ,
                             x = str(r.southwest.x),
                             y = str(r.southwest.y),
                             width=str(r.width),
                             height=str(r.height))
        
        text_style = self.parse_text_style(style)
        text_style.update({ "width": f"{r.width - 4}px",
                            "text-align" : "center",
                            "position":"absolute",
                            "top": "50%",
                            "transform" : "translateY(-50%)",
                            "padding": "0"
                            })
        
        text_node = ET.Element("xhtml:input", style=";".join(f"{key}:{text_style[key]}" for key in text_style),
                               type="text", value=str(text))
        foreign.append(text_node)
        self.add_to_layer(z_index, foreign)
        
        
    
