""" The Layer module """
# pylint: disable=invalid-name
import math
from abc import ABC, abstractmethod
from .Geometry import Transform

class Layer(ABC):
    """Layer is the abstract class that represents a graphics system.
    All relevant classes are subclasses of this one.

    :param transform: the general transform to apply to the layer
    :type transform: Transform
    
    """

    def __init__(self, transform = None):
        if transform is None:
            transform = Transform()
        self.transform = transform

    @abstractmethod
    def line(self, p1, p2, labels=None, **style):
        """ Draw a line from one point to the other (edge command)

        :param p1: the first point
        :type p1: Point
        :param p2: the second point
        :type p2: Point
        :param labels: dictionary of possible labels to put on the line
        :type labels: dict
        :param style: additional styling elements
        :type style: dict

        """


    @abstractmethod
    def text(self, point, text, **style):
        """Place a text at a given point (shape command)

        :param point: the point where the text will be placed
        :type point: Point
        :param text: The text
        :type text: str
        :param style: additional styling elements for the text
        :type style: dict

        The position of the text is affected by the transform, but the text
        itself is not: it will always appear horizontally and will not be
        stretched.
        """

    @abstractmethod
    def rectangle(self, p1, p2, **style):
        """Draws a rectangle whose corners are the two given points (shape command)

        :param p1: one of the corner of the rectangle
        :type p1: Point
        :param p2: the other corner of the rectangle
        :type point: Point
        :param style: additional styling elements for the rectangle
        :type style: dict

        The rectangle is affected by the transform: If the transform
        specifies that everything is rotated, then the rectangle will
        be rotated as well.
        """

    @abstractmethod
    def polyline(self, points, labels=None, closed=False, **style):
        """Draw line segments from one point to the next (edge command)

        :param points: list of points
        :type points: List[Point]
        :param labels: possible labels to put on the lines
        :type labels: dict
        :param closed: If true, draws a last line segment from the last point to the first point.
        :type closed: bool
        :param style: additional styling elements
        :type style: dict

        ``closed = True`` is slightly different from adding the
        first point as the last point.

        Here is an example. Let ``p0`` be the first point, ``p1`` the
        second point, and ``px`` the last point.  If ``closed =
        False`` and we add explicitely ``p0`` again at the end of the
        list of points, then a straight line would be drawn from
        ``px`` to ``p0`` and one from ``p0`` to ``p1``. However, the
        two lines intersecting at ``p0`` will not be considered a
        corner.  If one of the styling element involves the corner to
        be rounded, this corner would not be rounded.

        In general, it is therefore best to use ``closed = True`` for
        closed polylines.
        """

    @abstractmethod
    def polygon(self, points,  **style):
        """Draw a polygon (shape command)

        :param points: list of points
        :type points: List[Point]
        :param style: additional styling elements
        :type style: dict

        Internally, there is not a lot of difference between a polygon and a polyline, except polylines are lines (and therefore drawn first) while polygons are considered shaped (and therefore drawn last)        

        """
        
    @abstractmethod
    def circle(self, p1, radius, labels=None, **style):
        """Draws a circle given a point and a radius (shape command)

        :param p1: center of the circle
        :type point: Point
        :param radius: radius of the circle
        :type radius: float
        :param labels: possible labels to put on the circle
        :type labels: dict
        :param style: additional styling elements
        :type style: dict

        The circle is affected by the transform.
        It becomes an ellipse if for instance we use different scales
        for the x-axis and the y-axis.

        """

    @abstractmethod
    def edge(self, points, labels=None, closed = False, **style):
        """Draw a curve passing through the points (edge command)

        :param points: list of points
        :type points: List[Point]
        :param labels: possible labels to put on the lines
        :type labels: dict
        :param style: additional styling elements
        :type style: dict
        :param closed: If true, draws a last line segment from the last point to the first point.
        :type closed: bool

        
        The points might be decorated to specify at which angle the curve
        should pass through the point.
        """

    @abstractmethod
    def shape(self, points,  **style):
        """Draw a shape passing through the points (shape command)

        :param points: list of points
        :type points: List[Point]
        :param style: additional styling elements
        :type style: dict

        The points might be decorated to specify at which angle the curve
        should pass through the point.
        """
        

        
    @abstractmethod
    def picture(self, point, img_name, width, height):
        """Draw an image (shape command)

        :param point: where the image should be put
        :type point: Point
        :param img_name: path to the image
        :type img_name: str
        :param width: width of the image
        :type width: int
        :param height: height of the image
        :type height: int
        """
        
        pass

    @abstractmethod
    def draw(self, rect, fs=None, options=None, preamble=False):
        """Write the result in a file

        :param rect: The bounding box for the picture
        :type rect: Rectangle
        :param fs: A file I/O where to write the result
        :type fs: IO
        :param preamble: whether to produce a standalone document, or a document to be included in another
        :type preamble: bool

        """
        
        pass

    def find_angles(self, points, closed = False):
        """ Helper function: find the angles for the wires """

        def in_angle(node1, node2):
            c1 = node1
            c2 = node2
            x = c2.x - c1.x
            y = c2.y - c1.y
            angle = math.atan2(y, x) * 180 / math.pi
            return round(angle)

        the_list = []
        todraw = points
        current_node = todraw[0]
        current_hint = current_node.get('angle')
        next_node = todraw[1]
        angle = current_hint
        if angle is None:
            if not closed:            
                angle = in_angle(current_node, next_node)
            else:
                angle = in_angle(todraw[-1], next_node)
        the_list += [angle]
        for i in range(len(points) - 1):
            prev_node = todraw[i]
            current_node = todraw[i + 1]
            current_hint = current_node.get('angle')
            if i != len(points) - 2:
                next_node = todraw[i + 2]
            else:
                if not closed:
                    next_node = None
                else:
                    next_node = todraw[0]
            if current_hint is None:
                new_angle = in_angle(
                    prev_node,
                    next_node if next_node is not None else current_node)
            else:
                new_angle = current_hint
            the_list += [new_angle]
            angle = new_angle
        return the_list


class NoLayer(Layer):
    """ Dummy Layer that does nothing """
    def __init__(self, transform = None):
        Layer.__init__(self, transform)

    def line(self, p1, p2, labels=None, **style):
        pass

    def text(self, point, text, **style):
        pass

    def rectangle(self, p1, p2, **style):
        pass

    def circle(self, p1, radius, labels=None, **style):
        pass

    def picture(self, point, img_name, width, height):
        pass

    def draw(self, rect, fs=None, options=None, preamble=False):
        pass

    def polyline(self, points, labels=None, closed=False, **style):
        pass

    def polygon(self, points,  **style):
        pass
    
    def edge(self, points, labels=None, **style):
        pass

    def shape(self, points, **style):
        pass
    

class MultiLayer(Layer):
    """represents multiple layers at once

    :param layers: the list of layers 
    :type layers: List[Layer]


    The draw function has a different prototype, to take into account the different layers.
    
    """
    def __init__(self, layers):
        Layer.__init__(self, None)
        self.layers = layers

    def line(self, p1, p2, labels=None, **style):
        for layer in self.layers:
            layer.line(p1, p2, labels, **style)

    def text(self, point, text, **style):
        for layer in self.layers:
            layer.text(point, text, **style)

    def rectangle(self, p1, p2, **style):
        for layer in self.layers:
            layer.rectangle(p1, p2, **style)

    def circle(self, p1, radius, labels=None, **style):
        for layer in self.layers:
            layer.circle(p1, radius, labels, **style)

    def edge(self, points, labels=None, **style):
        for layer in self.layers:
            layer.edge(points, labels, **style)

    def shape(self, points,  **style):
        for layer in self.layers:
            layer.shape(points,  **style)
            
    def polyline(self, points, labels=None, closed=False, **style):
        for layer in self.layers:
            layer.polyline(points, labels, closed, **style)

    def polygon(self, points,  **style):
        for layer in self.layers:
            layer.polygon(points, **style)
            
    def picture(self, point, img_name, width, height):
        for layer in self.layers:
            layer.picture(point, img_name, width, height)

    def draw(self, rect, files=None, options=None, preamble=False):
        """Write the result to a list of files

        :param rect: The bounding box for the picture
        :type rect: Rectangle
        :param fs: A list of file I/O where to write the result
        :type fs: List[IO]
        :param preamble: whether to produce standalone documents, or documents to be included in another
        :type preamble: bool

        """
        
        if files is not None:
            for (layer, fs) in zip(self.layers, files):
                layer.draw(rect, fs, options, preamble)
        else:
            for layer in self.layers:
                layer.draw(rect, None, options, preamble)
