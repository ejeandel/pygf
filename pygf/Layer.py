import math
from abc import ABC, abstractmethod
from .Geometry import Point



class Node:
    """ A node has a position (a Diagram.Geometry.Point) and a style
    """

    def __init__(self, position, style = None):
        self.position = position
        if style is not None:
            self.style = style
        else:
            self.style = {}
        pass

    def __str__(self):
        return f"{self.position} {self.style}"
    
class Wire:
    """A wire represents a succession of points, and is associated with a certain style

    :param point: the first point on the wire
    :type point: Point
    :param angle: the angle 
    :type angle: float, optional
    :param wire_style: the style of the wire
    :type wire_style: dict

    .. todo::
       Point

"""
    __slots__ = ('l', 'wire_style')
    def __init__(self,point,angle=None, wire_style=None):
        if wire_style is None:
            raise TypeError
        if type(wire_style) != dict:
            raise TypeError
        self.l = [(point,angle)]
        self.wire_style = wire_style

    def add(self, point,angle=None):
        """add a point to the wire, same arguments as the constructor        
        """
        if type(point) == int:
            raise oups
        self.l += [(point,angle)]
        
    def __len__(self):
        return len(self.l)

    def __getitem__(self, x):
        return self.l[x]


class Layer(ABC):
    """Abstract class that represents a graphics system

    From the point of view of this class, a graphic system can represent:
    - Text 
    - Nodes, possibly with a label
    - Edges, that can connect nodes, possibly with a given orientation (an angle)             
    .. todo::
       parameters of style

    """
    
    __slots__ = ('nodes')
    def __init__(self):
        self.nodes = {}

    @abstractmethod
    def line(self, p1, p2, labels = None, style = None):        
        pass
    
    @abstractmethod
    def text(self, text):
        pass

    @abstractmethod
    def rectangle(self, p1, p2, **style):
        pass

    @abstractmethod
    def circle(self, p1, radius, labels = None, **style):
        pass

    
    @abstractmethod
    def picture(self, point, img_name, width, height):
        pass
    
    def writeStyle(f):
        pass


    def new_node(self, node):
        pass
        #self.nodes[name] = node


    def draw(self, r, fs= None, commands = "", preamble = False):
        pass
    pass

    def find_angles(self, points):
        def in_angle(node1, node2):
            c1 = node1
            c2 = node2
            x = c2[0] - c1[0]
            y = c2[1] - c1[1]
            angle = math.atan2(y,x)*180/math.pi
            return round(angle)
        
        """ Helper function: find the angles for the wires """
        l = []
        todraw = points
        (current_node, current_hint) = todraw[0]
        (next_node, next_hint) = todraw[1]
        angle = current_hint
        if angle is None:
            angle = in_angle(current_node, next_node)
        l += [angle]
        for i in range(len(points)-1):
            (prev_node, prev_hint) = todraw[i]
            (current_node, current_hint) = todraw[i+1]
            if i != len(points) - 2:
                (next_node, next_hint) = todraw[i+2]
            else:
                next_node = None
            if current_hint is None:
                new_angle = in_angle(prev_node, next_node if next_node is not None else current_node)
            else:
                new_angle = current_hint
            l += [new_angle]
            angle=new_angle
        return l

class NoLayer(Layer):
    def __init__(self):
        pass

    def line(self, p1, p2, labels = None, style = None):        
        pass
    
    def text(self, text):
        pass

    def rectangle(self, p1, p2, **style):
        pass

    def circle(self, p1, radius, labels = None, **style):
        pass
    
    def writeStyle(f):
        pass

    def new_node(self, node):
        pass

    def picture(self, point, img_name, width, height):
        pass
    
    def draw(self, r, fs= None, commands = "", preamble = False):
        pass

