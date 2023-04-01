""" Geometry classes """
# pylint: disable=invalid-name
import math
import copy


class Transform:
    r""" Codes a transformation matrix

    .. math::
      \begin{pmatrix}
      a & b & e \\
      c & d & f \\
      0 & 0 & 1
      \end{pmatrix}

    :param a,b,c,d,e,f: the coefficients. Defaults to the identity matrix
    :type a,b,c,d,e,f: float

    Three operators are defined on Transform objects:
      - one can multiply them together (using the * operator)
      - one can inverse a transform (using the inverse function)
      - one can apply the transform to a point

    """
    __slots__ = ('a', 'b', 'c', 'd', 'e', 'f')

    def __init__(self, a=1, b=0, c=0, d=1, e=0, f=0):
        # pylint: disable=too-many-arguments

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def __call__(self, point):
        """ transforms a point """

        x = self.a * point.x + self.b * point.y + self.e
        y = self.c * point.x + self.d * point.y + self.f

        return Point(x, y)

    def __mul__(self, other):
        """ composes two transforms """

        return Transform(self.a * other.a + self.b * other.c,
                         self.a * other.b + self.b * other.d,
                         self.c * other.a + self.d * other.c,
                         self.c * other.b + self.d * other.d,
                         self.a * other.e + self.b * other.f + self.e,
                         self.c * other.e + self.d * other.f + self.f)

    @property
    def inverse(self):
        """ returns the inverse of the transform """

        det = self.a * self.d - self.b * self.c

        return Transform(self.d / det, -self.b / det, -self.c / det,
                         self.a / det,
                         (self.b * self.f - self.d * self.e) / det,
                         (self.c * self.e - self.a * self.f) / det)

    @classmethod
    def Rotation(cls, angle):
        r""" returns the transform corresponding to a rotation

        Corresponds to the matrix

        .. math::
          \begin{pmatrix}
          \cos(\theta) & \sin(\theta) & 0 \\
          -\sin(\theta) & \cos(\theta) & 0 \\
          0 & 0 & 1
          \end{pmatrix}

        where :math:`\theta` is the angle of rotation.

        :param angle: the angle of rotation, expressed in radians
        :type angle: float

        """

        return cls(math.cos(angle), math.sin(angle), -math.sin(angle),
                   math.cos(angle))

    @classmethod
    def Scale(cls, x=1, y=1):
        r""" returns the transform corresponding to a rescaling

        Corresponds to the matrix

        .. math::
          \begin{pmatrix}
          x & 0 & 0 \\
          0 & y & 0 \\
          0 & 0 & 1
          \end{pmatrix}

        :param x,y: the x-axis and y-axis scales respectively
        :type x,y: float

        """
        return cls(a=x, d=y)


class Point:
    """ The famous Point class. Represents a point in 2D.

    Can be constructed either by giving the x-coordinate
    and the y-coordinate, or (if `polar=True`) by giving
    the radius and the angle (in radians).


    The point can be *decorated*, with additional attributes. Using the syntax
    `p@dict`, one can add all elements of the dictionary `dict`
    to the point `p`.

    If `p` is a point, the x and y coordinate can be accessed with
    `p.x` and `p.y` or by `p[0]` and `p[1]`.


    The following operators are defined on points :

      - Addition
      - Substraction
      - Multiplication by a float
      - Or-ing. The or of two points `A|B` is the point which has
        the same horizontal position as `A` and the same vertical position
        as `B`.

    Points can be converted to strings
    """

    __slots__ = ('x', 'y', 'dico')

    def __init__(self, fst, snd, polar=False):
        if polar is False:
            self.x = fst
            self.y = snd
        else:
            self.x = fst * math.cos(snd)
            self.y = fst * math.sin(snd)
        self.dico = {}

    def __matmul__(self, dico):
        x = copy.deepcopy(self)
        x.dico.update(dico)
        return x

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        return self.dico[key]

    def get(self, key, default=None):
        """ returns the decoration corresponding to key, like in a
        normal dictionary """

        return self.dico.get(key, default)

    def distance(self, p):
        """ returns the distance between this point and another point

        :param p: the other point
        :type p: Point
        """
        return math.hypot(self.x - p.x, self.y - p.y)

    @property
    def angle(self):
        """ returns the angle (in radians) between the point (0,0)
        and the point itself """

        return math.atan2(self.y, self.x)

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __rmul__(self, m):
        return Point(m * self.x, m * self.y)

    def __mul__(self, m):
        return Point(m * self.x, m * self.y)

    def __or__(self, p):
        return Point(self.x, p.y)

    def __format__(self, format_spec):
        return f"{self.x:.3f},{self.y:.3f}"

    def __str__(self):
        return self.__format__(None)


class Rectangle:
    """ The famous Rectangle class. The rectangle is aligned with the
    x-axis and the y-axis, and is given by two points.

    :param fst,snd: the two points
    :type fst,snd: Point

    """
    __slots__ = ('fst', 'snd')

    def __init__(self, fst, snd):
        if fst.x > snd.x:
            (x1, x2) = (snd.x, fst.x)
        else:
            (x1, x2) = (fst.x, snd.x)

        if fst.y > snd.y:
            (y1, y2) = (snd.y, fst.y)
        else:
            (y1, y2) = (fst.y, snd.y)

        self.fst = Point(x1, y1)
        self.snd = Point(x2, y2)

    def __str__(self):
        return self.fst.__str__() + " <-> " + self.snd.__str__()

    def __repr__(self):
        return self.fst.__str__() + " <-> " + self.snd.__str__()

    def __getitem__(self, key):
        if key == 0:
            return self.fst
        if key == 1:
            return self.snd
        raise IndexError

    def __contains__(self, p):
        return self.fst.x <= p.x <= self.snd.x and \
            self.fst.y <= p.y <= self.snd.y

    @property
    def center(self):
        """ returns the center of the rectangle

        :rtype: Point
        """

        return Point((self.fst.x + self.snd.x) / 2,
                     (self.fst.y + self.snd.y) / 2)

    @property
    def width(self):
        """ returns the width of the rectangle

        :rtype: float
        """

        return self.snd.x - self.fst.x

    @property
    def height(self):
        """ returns the height of the rectangle

        :rtype: float
        """

        return self.snd.y - self.fst.y

    @property
    def southwest(self):
        """ returns the southwest corner of the rectangle

        :rtype: Point
        """
        return self.fst

    @property
    def south(self):
        """ returns the point at the center of the south side of the rectangle

        :rtype: Point
        """
        return Point((self.fst.x + self.snd.x) / 2, self.fst.y)

    @property
    def north(self):
        """ returns the point at the center of the north side of the rectangle

        :rtype: Point
        """
        return Point((self.fst.x + self.snd.x) / 2, self.snd.y)

    @property
    def northwest(self):
        """ returns the northwest corner of the rectangle

        :rtype: Point
        """
        return Point(self.fst.x, self.snd.y)

    @property
    def northeast(self):
        """ returns the northeast corner of the rectangle

        :rtype: Point
        """
        return self.snd

    @property
    def southeast(self):
        """ returns the southeast corner of the rectangle

        :rtype: Point
        """
        return Point(self.snd.x, self.fst.y)

    @classmethod
    def bounding_box(cls, point_list):
        """ returns the smallest rectangle that contains all points
        in the list.

        :param point_list: The list of points
        :type point_list: List[Point]

        :rtype: Rectangle
        """
        x0 = x1 = point_list[0].x
        y0 = y1 = point_list[0].y
        for p in point_list[1:]:
            if p.x < x0:
                x0 = p.x
            if p.x > x1:
                x1 = p.x
            if p.y < y0:
                y0 = p.y
            if p.y > y1:
                y1 = p.y
        return cls(Point(x0, y0), Point(x1, y1))
