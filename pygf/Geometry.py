import math
import copy
""" The Transform class """


class Transform:
    """ Codes a matrix
    (a b e)
    (c d f)
    (0 0 1)
    """
    __slots__ = ('a', 'b', 'c', 'd', 'e', 'f')

    def __init__(self, x=1, y=1):
        self.a = x
        self.b = 0
        self.c = 0
        self.d = y
        self.e = 0
        self.f = 0

    def __call__(self, point):
        x = self.a * point.x + self.b * point.y + self.e
        y = self.c * point.x + self.d * point.y + self.f

        return Point(x, y)

    def __mul__(self, other):
        result = Transform()
        result.a = self.a * other.a + self.b * other.c
        result.b = self.a * other.b + self.b * other.d
        result.c = self.c * other.a + self.d * other.c
        result.d = self.c * other.b + self.d * other.d
        result.e = self.a * other.e + self.b * other.f + self.e
        result.f = self.c * other.e + self.d * other.f + self.f
        return result

    @property
    def inverse(self):
        result = Transform(1, 1)

        det = self.a * self.d - self.b * self.c

        result.a = self.d / det
        result.b = -self.b / det
        result.c = -self.c / det
        result.d = self.a / det
        result.e = (self.b * self.f - self.d * self.e) / det
        result.f = (self.c * self.e - self.a * self.f) / det

        return result

    def Rotation(angle):
        x = Transform()
        x.a = x.d = math.cos(angle)
        x.b = math.sin(angle)
        x.c = -x.b
        return x


""" The famous Point class """


class Point:
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
        elif key == 1:
            return self.y
        else:
            return self.dico[key]

    def get(self, key, default=None):
        return self.dico.get(key, default)

    def distance(self, p):
        return math.hypot(self.x - p.x, self.y - p.y)

    @property
    def angle(self):
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
        return "%.3f,%.3f" % (self.x, self.y)

    def __str__(self):
        return self.__format__(None)


""" The famous Rectangle class """


class Rectangle:
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
        elif key == 1:
            return self.snd
        else:
            raise IndexError

    def __contains__(self, p):
        return self.fst.x <= p.x <= self.snd.x and \
            self.fst.y <= p.y <= self.snd.y

    @property
    def center(self):
        return Point((self.fst.x + self.snd.x) / 2,
                     (self.fst.y + self.snd.y) / 2)

    @property
    def width(self):
        return self.snd.x - self.fst.x

    @property
    def height(self):
        return self.snd.y - self.fst.y

    @property
    def southwest(self):
        return self.fst

    @property
    def south(self):
        return Point((self.fst.x + self.snd.x) / 2, self.fst.y)

    @property
    def north(self):
        return Point((self.fst.x + self.snd.x) / 2, self.snd.y)

    @property
    def northwest(self):
        return Point(self.fst.x, self.snd.y)

    @property
    def northeast(self):
        return self.snd

    @property
    def southeast(self):
        return Point(self.snd.x, self.fst.y)

    def frac(self, x, y):
        return Point(
            (self.fst.x + self.snd.x) / 2 + x * (self.snd.x - self.fst.x) / 2,
            (self.fst.y + self.snd.y) / 2 + y * (self.snd.y - self.fst.y) / 2)

    def fit(self, width, height):
        """ returns a subrectangle of size (width, height)
        centered in the rectangle"""
        if self.width > width:
            x1, x2 = (self.fst.x + self.snd.x -
                      width) / 2, (self.fst.x + self.snd.x + width) / 2
        else:
            x1, x2 = self.fst.x, self.snd.x
        if self.height > height:
            y1, y2 = (self.fst.y + self.snd.y -
                      height) / 2, (self.fst.y + self.snd.y + height) / 2
        else:
            y1, y2 = self.fst.y, self.snd.y
        return Rectangle(Point(x1, y1), Point(x2, y2))

    def vertical_split(self, the_list):
        """ l is a list of weights of size n
        split the rectangle into n rectangles
        in such a way that the width of each rectangle
        is proportional to its weight
        if l = [1,1], we obtain two rectangles of equal width
        if l = [1,2], the second rectangle is twice as big
        """
        total_weight = sum(the_list)
        x1 = self.fst.x
        x2 = self.snd.x
        height = self.snd.y - self.fst.y
        output = []
        cumulative_weight = 0
        for i in the_list:
            y1 = self.fst.y + cumulative_weight * height / total_weight
            cumulative_weight += i
            y2 = self.fst.y + cumulative_weight * height / total_weight
            output += [Rectangle(Point(x1, y1), Point(x2, y2))]
        return output

    def horizontal_split(self, the_list):
        """ same as the previous function, but horizontally
        """
        total_weight = sum(the_list)
        y1 = self.fst.y
        y2 = self.snd.y
        width = self.snd.x - self.fst.x
        output = []
        cumulative_weight = 0
        for i in the_list:
            x1 = self.fst.x + cumulative_weight * width / total_weight
            cumulative_weight += i
            x2 = self.fst.x + cumulative_weight * width / total_weight
            output += [Rectangle(Point(x1, y1), Point(x2, y2))]
        return output

    def bounding_box(the_list):
        """ returns the smallest rectangle that contains all points in l """
        x0 = x1 = the_list[0].x
        y0 = y1 = the_list[0].y
        for p in the_list[1:]:
            if p.x < x0:
                x0 = p.x
            if p.x > x1:
                x1 = p.x
            if p.y < y0:
                y0 = p.y
            if p.y > y1:
                y1 = p.y
        return Rectangle(Point(x0, y0), Point(x1, y1))
