"""Geometry classes"""

# pylint: disable=invalid-name
from __future__ import annotations
import math
import copy
from typing import Dict, Any, List


class Point:
    """The famous Point class. Represents a point in 2D.

    Can be constructed either by giving the x-coordinate
    and the y-coordinate, or (if `polar=True`) by giving
    the radius and the angle (in radians).


    The point can be *decorated*, with additional attributes. Using the syntax
    `p@dict`, one can add all elements of the dictionary `dict`
    to the point `p`.

    If `p` is a point, the x and y coordinate can be accessed with
    `p.x` and `p.y`.


    The following operators are defined on points :

      - Addition
      - Substraction
      - Multiplication by a float
      - Or-ing. The or of two points `A|B` is the point which has
        the same horizontal position as `A` and the same vertical position
        as `B`.

    Points can be converted to strings.

    :param fst: the x coordinate (if `polar=False`) or the radius (if `polar=True`).
    :param snd: the y coordinate (if `polar=False`) or the angle (if `polar=True`).
    :param polar: True if parameters are polar coordinates rather than xy-coordinates.

    """

    __slots__ = ("x", "y", "dico")

    def __init__(self, fst: float, snd: float, polar: bool = False):
        if polar is False:
            self.x = fst
            self.y = snd
        else:
            self.x = fst * math.cos(snd)
            self.y = fst * math.sin(snd)
        self.dico: Dict[str, Any] = {}

    def __matmul__(self, dico: Dict[str, Any]) -> Point:
        x = copy.deepcopy(self)
        x.dico.update(dico)
        return x

    def get(self, key: str, default: Any = None) -> Any:
        """returns the decoration corresponding to key, like in a
        normal dictionary"""

        return self.dico.get(key, default)

    def distance(self, p: Point) -> float:
        """returns the distance between this point and another point

        :param p: the other point
        """
        return math.hypot(self.x - p.x, self.y - p.y)

    @property
    def angle(self) -> float:
        """returns the angle (in radians) between the point (0,0)
        and the point itself"""

        return math.atan2(self.y, self.x)

    def __add__(self, p: Point) -> Point:
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p: Point) -> Point:
        return Point(self.x - p.x, self.y - p.y)

    def __rmul__(self, m: float) -> Point:
        return Point(m * self.x, m * self.y)

    def __mul__(self, m: float) -> Point:
        return Point(m * self.x, m * self.y)

    def __or__(self, p: Point) -> Point:
        return Point(self.x, p.y)

    def __format__(self, format_spec: str | None) -> str:
        return f"{self.x:.3f},{self.y:.3f}"

    def __str__(self) -> str:
        return self.__format__(None)


class Rectangle:
    """The famous Rectangle class. The rectangle is aligned with the
    x-axis and the y-axis, and is given by two points.

    :param fst: one corner of the rectangle
    :param snd: opposite corner of the rectangle

    """

    __slots__ = ("fst", "snd")

    def __init__(self, fst: Point, snd: Point):
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

    def __str__(self) -> str:
        return self.fst.__str__() + " <-> " + self.snd.__str__()

    def __repr__(self) -> str:
        return self.fst.__str__() + " <-> " + self.snd.__str__()

    def __getitem__(self, key: int) -> Point:
        if key == 0:
            return self.fst
        if key == 1:
            return self.snd
        raise IndexError

    def __contains__(self, p: Point) -> bool:
        return self.fst.x <= p.x <= self.snd.x and self.fst.y <= p.y <= self.snd.y

    @property
    def center(self) -> Point:
        """returns the center of the rectangle

        :rtype: Point
        """

        return Point((self.fst.x + self.snd.x) / 2, (self.fst.y + self.snd.y) / 2)

    @property
    def width(self) -> float:
        """returns the width of the rectangle

        :rtype: float
        """

        return self.snd.x - self.fst.x

    @property
    def height(self) -> float:
        """returns the height of the rectangle

        :rtype: float
        """

        return self.snd.y - self.fst.y

    @property
    def southwest(self) -> Point:
        """returns the southwest corner of the rectangle

        :rtype: Point
        """
        return self.fst

    @property
    def south(self) -> Point:
        """returns the point at the center of the south side of the rectangle

        :rtype: Point
        """
        return Point((self.fst.x + self.snd.x) / 2, self.fst.y)

    @property
    def north(self) -> Point:
        """returns the point at the center of the north side of the rectangle

        :rtype: Point
        """
        return Point((self.fst.x + self.snd.x) / 2, self.snd.y)

    @property
    def northwest(self) -> Point:
        """returns the northwest corner of the rectangle

        :rtype: Point
        """
        return Point(self.fst.x, self.snd.y)

    @property
    def northeast(self) -> Point:
        """returns the northeast corner of the rectangle

        :rtype: Point
        """
        return self.snd

    @property
    def southeast(self) -> Point:
        """returns the southeast corner of the rectangle

        :rtype: Point
        """
        return Point(self.snd.x, self.fst.y)

    @classmethod
    def bounding_box(cls: type[Rectangle], point_list: List[Point]) -> Rectangle:
        """returns the smallest rectangle that contains all points
        in the list.

        :param point_list: The list of points
        :type point_list: List[Point]

        :rtype: Rectangle
        """
        x0 = min(map(lambda p: p.x, point_list))
        x1 = max(map(lambda p: p.x, point_list))
        y0 = min(map(lambda p: p.y, point_list))
        y1 = max(map(lambda p: p.y, point_list))
        return cls(Point(x0, y0), Point(x1, y1))

    def vertical_split(self, weight_list: List[int]) -> List[Rectangle]:
        """
        given a list of weights, splits the rectangle into n rectangles
        in such a way that the width of each rectangle is proportional to its weight

        :param weight_list: list of coefficients
        :type weight_list: List[int]

        """
        total_weight = sum(weight_list)
        x1 = self.fst.x
        x2 = self.snd.x
        height = self.snd.y - self.fst.y
        output = []
        cumulative_weight = 0
        for i in weight_list:
            y1 = self.fst.y + cumulative_weight * height / total_weight
            cumulative_weight += i
            y2 = self.fst.y + cumulative_weight * height / total_weight
            output += [Rectangle(Point(x1, y1), Point(x2, y2))]
        return output

    def horizontal_split(self, weight_list: List[int]) -> List[Rectangle]:
        """
        given a list of weights, splits the rectangle into n rectangles
        in such a way that the height of each rectangle is proportional to its weight

        :param weight_list: list of coefficients
        :type weight_list: List[int]

        """
        total_weight = sum(weight_list)
        y1 = self.fst.y
        y2 = self.snd.y
        width = self.snd.x - self.fst.x
        output = []
        cumulative_weight = 0
        for i in weight_list:
            x1 = self.fst.x + cumulative_weight * width / total_weight
            cumulative_weight += i
            x2 = self.fst.x + cumulative_weight * width / total_weight
            output += [Rectangle(Point(x1, y1), Point(x2, y2))]
        return output

    def fit(self, width: int, height: int) -> Rectangle:
        """
        returns a subrectangle of size (width, height) centered in the rectangle

        :param width: width of the sub-rectangle
        :type width: int

        :param height: height of the sub-rectangle
        :type height: int

        """
        if self.width > width:
            x1 = (self.fst.x + self.snd.x - width) / 2
            x2 = (self.fst.x + self.snd.x + width) / 2
        else:
            x1, x2 = self.fst.x, self.snd.x
        if self.height > height:
            y1 = (self.fst.y + self.snd.y - height) / 2
            y2 = (self.fst.y + self.snd.y + height) / 2
        else:
            y1, y2 = self.fst.y, self.snd.y
        return Rectangle(Point(x1, y1), Point(x2, y2))


class Transform:
    r""" Codes a transformation matrix

    .. math::
      \begin{pmatrix}
      a & b & e \\
      c & d & f \\
      0 & 0 & 1
      \end{pmatrix}

    :param a: one coefficient (defaults to 1)
    :param b: one coefficient (defaults to 0)
    :param c: one coefficient (defaults to 0)
    :param d: one coefficient (defaults to 1)
    :param e: one coefficient (defaults to 0)
    :param f: one coefficient (defaults to 0)

    The six parameters by default corresponds to the Identity matrix.

    Three operators are defined on Transform objects:
      - one can multiply them together (using the * operator)
      - one can inverse a transform (using the inverse function)
      - one can apply the transform to a point

    """

    __slots__ = ("a", "b", "c", "d", "e", "f")

    def __init__(
        self,
        a: float = 1,
        b: float = 0,
        c: float = 0,
        d: float = 1,
        e: float = 0,
        f: float = 0,
    ):
        # pylint: disable=too-many-arguments

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def __call__(self, point: Point) -> Point:
        """transforms a point"""

        x = self.a * point.x + self.b * point.y + self.e
        y = self.c * point.x + self.d * point.y + self.f

        return Point(x, y)

    def __mul__(self, other: Transform) -> Transform:
        """composes two transforms"""

        return Transform(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d,
            self.a * other.e + self.b * other.f + self.e,
            self.c * other.e + self.d * other.f + self.f,
        )

    @property
    def inverse(self) -> Transform:
        """returns the inverse of the transform"""

        det = self.a * self.d - self.b * self.c

        return Transform(
            self.d / det,
            -self.b / det,
            -self.c / det,
            self.a / det,
            (self.b * self.f - self.d * self.e) / det,
            (self.c * self.e - self.a * self.f) / det,
        )

    @classmethod
    def Rotation(cls: type[Transform], angle: float) -> Transform:
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

        return cls(math.cos(angle), math.sin(angle), -math.sin(angle), math.cos(angle))

    @classmethod
    def Scale(cls: type[Transform], x: float = 1, y: float = 1) -> Transform:
        r""" returns the transform corresponding to a rescaling

        Corresponds to the matrix

        .. math::
          \begin{pmatrix}
          x & 0 & 0 \\
          0 & y & 0 \\
          0 & 0 & 1
          \end{pmatrix}

        :param x: the scale to apply to the x-axis
        :param y: the scale to apply to the y-axis

        """
        return cls(a=x, d=y)
