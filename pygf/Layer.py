import math
from abc import ABC, abstractmethod
from .Geometry import Point, Transform




class Layer(ABC):
    """Abstract class that represents a graphics system
    """
    
    def __init__(self, transform = None):
        if transform is None:
            transform = Transform()
        self.transform = transform

    @abstractmethod
    def line(self, p1, p2, labels = None, **style):        
        pass
    
    @abstractmethod
    def text(self, point, text, **style):
        pass

    @abstractmethod
    def rectangle(self, p1, p2, **style):
        pass

    @abstractmethod
    def circle(self, p1, radius, labels = None, **style):
        pass

    @abstractmethod
    def edge(self, points, labels = None, **style):
        pass

    @abstractmethod
    def polyline(self, points, labels = None, closed = False, **style):
        pass
    
    
    @abstractmethod
    def picture(self, point, img_name, width, height):
        pass
    
    @abstractmethod
    def draw(self, r, fs= None, commands = None, preamble = False):
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

    def line(self, p1, p2, labels = None, **style):        
        pass

    def text(self, point, text, **style):
        pass
    
    def rectangle(self, p1, p2, **style):
        pass

    def circle(self, p1, radius, labels = None, **style):
        pass
    
    def picture(self, point, img_name, width, height):
        pass
    
    def draw(self, r, fs= None, commands = None, preamble = False):
        pass

    def polyline(self, points, labels = None, closed = False,  **style):
        pass

    def edge(self, points, labels = None, **style):
        pass
    


class MultiLayer(Layer):
    def __init__(self, layers):
        self.layers = layers

    def line(self, p1, p2, labels = None, **style):        
        for layer in self.layers:
            layer.line(p1, p2, labels, **style)

    def text(self, point, text, **style):
        for layer in self.layers:
            layer.text(point, text, **style)

    def rectangle(self, p1, p2, **style):
        for layer in self.layers:
            layer.rectangle(p1, p2, **style)
        
    def circle(self, p1, radius, labels = None, **style):
        for layer in self.layers:
            layer.circle(p1, radius, labels, **style)

            
    def edge(self, points, labels = None, **style):
        for layer in self.layers:
            layer.edge(points, labels, **style)

    def polyline(self, points, labels = None, closed = False, **style):
        for layer in self.layers:
            layer.polyline(points, labels,closed,  **style)

    
    
    def picture(self, point, img_name, width, height):
        for layer in self.layers:
            layer.polyline(points, img_name, width, height)

    
    def draw(self, r, files= None, commands = None, preamble = False):
        if files is not None:
            for (layer,fs) in zip(self.layers,files):
                layer.draw(r, fs, commands, preamble)
        else:
            for layer in self.layers:
                layer.draw(r, None, commands, preamble)
        
