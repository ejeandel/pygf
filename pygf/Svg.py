"""Module that provides the SVG Layer"""

# pylint: disable=invalid-name
import math
import base64
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from .Layer import Layer
from .Geometry import Point, Rectangle, Transform


@dataclass
class PathElement:
    """
    represents one part of a SVG Path
    """

    first_point: Point
    next_point: Point

    def is_up(self):
        """
        determines if the path element is drawn from left to right
        or from right to left
        important to know how to draw the text
        """
        return abs((self.next_point - self.first_point).angle) > math.pi / 2

    def reverse(self):
        """
        return the reverse of the path element
        """
        return self


@dataclass
class SVGLine(PathElement):
    """A line element in a SVG Path"""

    def __str__(self, first=False):
        s = ""
        if first:
            s = "M {self.first_point}"
        s += f" L {self.next_point}"
        return s

    def reverse(self):
        return SVGLine(self.next_point, self.first_point)


@dataclass
class SVGEllipse(PathElement):
    """An ellipse element in a SVG Path"""

    rx: float
    ry: float
    x_axis_rotation: float
    large_flag: int
    sweep_flag: int

    def __str__(self, first=False):
        s = ""
        if first:
            s = "M {self.first_point}"
        s += (
            f" A {self.rx} {self.ry} {self.x_axis_rotation}"
            f" {self.large_flag} {self.sweep_flag} {self.next_point}"
        )
        return s

    def reverse(self):
        return SVGEllipse(
            self.next_point,
            self.first_point,
            self.rx,
            self.ry,
            self.x_axis_rotation,
            self.large_flag,
            1 - self.sweep_flag,
        )

    def is_up(self):
        return self.sweep_flag > 0


@dataclass
class SVGBezier(PathElement):
    """A Bezier curve element in a SVG Path"""

    first_control_point: Point
    second_control_point: Point

    def __str__(self, first=False):
        s = ""
        if first:
            s = "M {self.first_point}"
        s += f" C {self.first_control_point} {self.second_control_point} {self.next_point}"
        return s

    def reverse(self):
        return SVGBezier(
            self.next_point,
            self.first_point,
            self.second_control_point,
            self.first_control_point,
        )


@dataclass
class SVGQuadratic(PathElement):
    """A Quadratic Bezier curve element in a SVG Path"""

    control_point: Point

    def __str__(self, first=False):
        s = ""
        if first:
            s = "M {self.first_point}"
        s += f" Q {self.control_point} {self.next_point}"
        return s

    def reverse(self):
        return SVGQuadratic(self.next_point, self.first_point, self.control_point)


class SvgPath:
    """A path in SVG. Not all features are supported.

    Not implemented
      - relative commands
      - V/H (not worth it)
      - Z (cycle)
      - S (Reflected Bezier)
      - T (Reflected Quadratic Bezier)

    """

    def __init__(self, start_point, path_list=None):
        self.current_point = start_point
        if path_list is None:
            self.path_list = []
        else:
            self.path_list = path_list

    def line_to(self, next_point):
        """Adds a line from the current_point to the next point"""
        self.path_list += [SVGLine(self.current_point, next_point)]
        self.current_point = next_point

    def ellipse_to(self, next_point, rx, ry, x_axis_rotation, large_flag, sweep_flag):
        """Adds an ellipse"""
        self.path_list += [
            SVGEllipse(
                self.current_point,
                next_point,
                rx,
                ry,
                x_axis_rotation,
                large_flag,
                sweep_flag,
            )
        ]
        self.current_point = next_point

    def curve_to(self, next_point, first_control_point, second_control_point):
        """Adds a Bezier Curve"""
        self.path_list += [
            SVGBezier(
                self.current_point,
                next_point,
                first_control_point,
                second_control_point,
            )
        ]
        self.current_point = next_point

    def quadratic_to(self, next_point, control_point):
        """Adds a Quadratic Curve"""
        self.path_list += [SVGQuadratic(self.current_point, next_point, control_point)]
        self.current_point = next_point

    def __str__(self):
        first_point = self.path_list[0].first_point
        s = f"M {first_point}"
        return s + "".join(str(i) for i in self.path_list)

    def reverse(self):
        """return the reverse of the SVG path"""
        if len(self.path_list) == 0:
            return SvgPath(self.current_point)

        reverse_list = [x.reverse() for x in self.path_list[::-1]]
        last_point = reverse_list[-1].next_point
        return SvgPath(last_point, reverse_list)

    def is_up(self):
        """return whether the path is drawn from left to right
        or in the other direction"""
        if len(self.path_list) == 0:
            raise NotImplementedError

        return self.path_list[0].is_up()


def pt_to_cm(x):
    """converts pt to cm"""
    return x * 2.54 / 72.27


class SvgLayer(Layer):
    """the SVG Layer"""

    def __init__(self, transform=None):
        Layer.__init__(self, transform)
        self.names = 0
        # node = 1
        # edge = 0
        self.layers = {0: [], 1: []}
        self.defs = {}
        self.svgtransform = Transform(a=50, d=-50)

    def new_name(self):
        """return a new name for an id"""
        self.names += 1
        return f"{self.names}"

    def add_to_layer(self, z_index, x):
        """helper function"""
        if z_index not in self.layers:
            self.layers[z_index] = []
        self.layers[z_index].append(x)

    def picture(self, point, img_name, width, height, z_index=1):
        tf = self.svgtransform * self.transform
        r = Rectangle(Point(0, 0), self.svgtransform(Point(width, -height)))
        with open(img_name, "rb") as f:
            data = f.read()
            image_node = ET.Element("image", width=str(r.width), height=str(r.height))
            image_node.set(
                "xlink:href",
                f'data:image/png;base64,{str(base64.b64encode(data), "utf-8")}',
            )
            image_node.set("transform", f"translate({tf(point)-r.center})")
            image_node.set("preserveAspectRatio", "none")

            self.add_to_layer(z_index, image_node)

    def parse_stroke_width(self, style):
        """---------
        thickness
        ---------"""

        if "thickness" in style:
            thickness = style["thickness"]
            del style["thickness"]
        else:
            thickness = 1
        pt = pt_to_cm(1) * self.svgtransform(Point(1, 1)).x
        stroke_width = 0.4 * pt * thickness
        return stroke_width

    def parse_style(self, stroke_width, style, svg_style):
        # dash
        pt = pt_to_cm(1) * self.svgtransform(Point(1, 1)).x
        if "dash" in style:
            dash = style["dash"]
            del style["dash"]
            sw = stroke_width
            dasharray = {
                "solid": "none",
                "dotted": f"{sw:.2g} {2*pt:.2g}",
                "densely dotted": f"{sw:.2g} {1*pt:.2g}",
                "loosely dotted": f"{sw:.2g} {4*pt:.2g}",
                "dashed": f"{3*pt:.2g}",
                "densely dashed": f"{3*pt:.2g} {2*pt:.2g}",
                "loosely dashed": f"{3*pt:.2g} {6*pt:.2g}",
                "dashdotted": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "dash dot": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dashdotted": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "densely dash dot": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dashdotted": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "loosely dash dot": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "dashdotdotted": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dashdotdotted": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dashdotdotted": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "dash dot dot": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dash dot dot": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dash dot dot": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
            }.get(dash)
            svg_style["stroke-dasharray"] = dasharray
        # draw
        if "draw" in style:
            color = style["draw"]
            del style["draw"]
            if color is None:
                color = "none"
        else:
            color = "black"
        svg_style["stroke"] = color
        # fill
        if "fill" in style:
            fill = style["fill"]
            del style["fill"]
            if fill is None:
                fill = "none"
            if "opacity" in style:
                svg_style["fill-opacity"] = style["opacity"]
                del style["opacity"]
        else:
            fill = "none"
        svg_style["fill"] = fill

        if "rounded" in style and style["rounded"]:
            del style["rounded"]
            svg_style["stroke-linejoin"] = "round"

    def parse_text_style(self, style, text_style):
        """internal function
        computes the text attributes
        """
        if "text_size" in style:
            if style["text_size"] == "small":
                text_style["font-size"] = "x-small"
            if style["text_size"] == "large":
                text_style["font-size"] = "x-large"
            del style["text_size"]

        if "font_family" in style:
            text_style["font-family"] = style["font_family"]
            del style["font_family"]
        else:
            text_style["font-family"] = "sans-serif"

        if "text_color" in style:
            text_style["stroke"] = style["text_color"]
            del style["text_color"]

    def parse_arrows(self, stroke_width, style, svg, sub_path):
        """internal function for arrows"""
        if "arrow" not in style:
            return
        pt = pt_to_cm(1) * self.svgtransform(Point(1, 1)).x

        arrows = style["arrow"].split("-")

        def latex_arrow(reverse=False, first=False):
            x = 0.28 * pt + 0.3 * stroke_width

            width = 11 * x
            height = 10 * x

            X = -x if not reverse else x
            if not first:
                refX = width - 0.5 * stroke_width
            else:
                refX = 0.5 * stroke_width

            arrow = ET.Element(
                "marker",
                markerUnits="userSpaceOnUse",
                markerWidth=str(width),
                markerHeight=str(height),
                refX=str(refX),
                refY=str(height / 2),
                orient="auto",
            )
            arrow.set("stroke-width", str(stroke_width))

            relative = Point(-width if not reverse else 0, -height / 2)
            arrow_path = SvgPath(Point(0, 0) - relative)
            arrow_path.curve_to(
                Point(10 * X, 3.75 * x) - relative,
                Point(8 * X / 3, 0.5 * x) - relative,
                Point(7 * X, 2 * x) - relative,
            )
            arrow_path.line_to(Point(10 * X, -3.75 * x) - relative)
            arrow_path.curve_to(
                Point(0, 0) - relative,
                Point(7 * X, -2 * x) - relative,
                Point(8 * X / 3, -0.5 * x) - relative,
            )
            arrow_svg_path = ET.Element("path", d=str(arrow_path), fill=svg.get("stroke"))
            arrow.append(arrow_svg_path)
            return arrow

        def default_arrow(reverse=False, first=False):
            x = 0.28 * pt + 0.3 * stroke_width
            width = 5 * x
            height = 10 * x
            X = -x if not reverse else x
            if not reverse:
                refX = width - 0.4 * stroke_width
            else:
                refX = 0.4 * stroke_width
            arrow = ET.Element(
                "marker",
                markerUnits="userSpaceOnUse",
                markerWidth=str(width),
                markerHeight=str(height),
                refX=str(refX),
                refY=str(height / 2),
                orient="auto",
            )
            arrow.set("stroke-width", str(0.8 * stroke_width))
            relative = Point(-width if not reverse else 0, -height / 2)
            arrow_path = SvgPath(Point(3.75 * X, 4 * x) - relative)
            arrow_path.curve_to(
                Point(0, 0) - relative,
                Point(3.5 * X, 2.5 * x) - relative,
                Point(0.75 * X, 0.25 * x) - relative,
            )
            arrow_path.curve_to(
                Point(3.75 * X, -4 * x) - relative,
                Point(0.75 * X, -0.25 * x) - relative,
                Point(3.5 * X, -2.5 * x) - relative,
            )
            arrow_svg_path = ET.Element("path", d=str(arrow_path))
            arrow_svg_path.set("stroke-linecap", "round")
            arrow_svg_path.set("stroke-linejoin", "round")
            arrow_svg_path.set("stroke-dasharray", "none")
            arrow.append(arrow_svg_path)
            return arrow

        def x_arrow(reverse=False, first=False):
            width = 3 * pt + 4 * stroke_width

            arrow = ET.Element(
                "marker",
                markerUnits="userSpaceOnUse",
                markerWidth=str(width),
                markerHeight=str(width),
                refX=str(width / 2),
                refY=str(width / 2),
                orient="auto",
            )

            arrow.append(ET.Element("polyline", points=f"{Point(0, 0)} {Point(width, width)}"))
            arrow.append(ET.Element("polyline", points=f"{Point(width, 0)} {Point(0, width)}"))
            return arrow

        for i in range(2):
            if arrows[i] == "":
                continue
            
            if arrows[i] == ">":
                arrow = default_arrow(False, i == 0)
            elif arrows[i] == "<":
                arrow = default_arrow(True, i == 0)
            elif arrows[i] == "latex":
                arrow = latex_arrow(False, i == 0)
            elif arrows[i] == "xetal":
                arrow = latex_arrow(True, i == 0)
            elif arrows[i] == "x":
                arrow = x_arrow(False, False)
            else:
                raise NotImplementedError(arrows[i])

            
            _id = self.new_name()
            sub_path.set("marker-start" if i == 0 else "marker-end", f"url(#marker_{_id})")
            arrow.set("id", f"marker_{_id}")
            svg.append(arrow)

    def __path(self, svg_path, labels=None, style=None, z_index=0):
        if style is None:
            style = {}

        reverse_start = svg_path.is_up()
        reverse_end = not svg_path.reverse().is_up()

        stroke_width = self.parse_stroke_width(style)

        svg_style = {"stroke-width": f"{stroke_width:2g}"}
        self.parse_style(stroke_width, style, svg_style)

        text_style = {}
        self.parse_text_style(style, text_style)

        _id = self.new_name()

        svg = ET.Element("g", svg_style)
        sub_path = ET.Element("path", id=_id, d=str(svg_path))
        svg.append(sub_path)

        self.parse_arrows(stroke_width, style, svg, sub_path)

        self.add_to_layer(z_index, svg)

        if labels is not None:
            need_reverse = False

            for position in labels:
                if "start" in position and reverse_start:
                    need_reverse = True
                if "end" in position and reverse_end:
                    need_reverse = True
                if (position == "above" and reverse_start) or (position == "below" and reverse_end):
                    need_reverse = True
            if need_reverse:
                self.add_to_layer(
                    z_index,
                    ET.Element("path", id=f"r-{_id}", d=str(svg_path.reverse()), display="none"),
                )

            for position in labels:
                text_svg = ET.Element("text", text_style)
                if "above" in position:
                    text_svg.set("dy", "-5")
                else:
                    # below
                    text_svg.set("dy", "5")
                    text_svg.set("dominant-baseline", "hanging")

                text_path = ET.Element("textPath")

                if "start" in position:
                    text_svg.set("text-anchor", "start" if not reverse_start else "end")
                    text_path.set("startOffset", "0%" if not reverse_start else "100%")
                    text_path.set("href", f"#{_id}" if not reverse_start else f"#r-{_id}")
                elif "end" in position:
                    text_svg.set("text-anchor", "end" if not reverse_end else "start")
                    text_path.set("startOffset", "100%" if not reverse_end else "0%")
                    text_path.set("href", f"#{_id}" if not reverse_end else f"#r-{_id}")
                else:
                    text_svg.set("text-anchor", "middle")
                    text_path.set("startOffset", "50%")
                    if position == "above":
                        text_path.set("href", f"#{_id}" if not reverse_start else f"#r-{_id}")
                    else:
                        text_path.set("href", f"#{_id}" if not reverse_end else f"#r-{_id}")

                text_path.text = str(labels[position])
                text_svg.append(text_path)
                self.add_to_layer(z_index, text_svg)

    def line(self, p1, p2, labels=None, z_index=0, **style):
        (p1, p2) = map(self.svgtransform * self.transform, (p1, p2))
        svg_path = SvgPath(p1)
        svg_path.line_to(p2)

        self.__path(svg_path, labels, style, z_index)

    def circle(self, p1, radius, labels=None, z_index=1, **style):
        tf = self.svgtransform * self.transform

        rx = tf(p1).distance(tf(Point(radius, 0) + p1))
        ry = tf(p1).distance(tf(Point(0, radius) + p1))

        x1 = tf(p1 + Point(radius, 0))
        x2 = tf(p1 - Point(radius, 0))

        x_axis_rotation = tf(Point(radius, 0)).angle * 180 / math.pi

        svg_path = SvgPath(x1)
        svg_path.ellipse_to(x2, rx, ry, x_axis_rotation, 1, 1)
        svg_path.ellipse_to(x1, rx, ry, x_axis_rotation, 1, 1)

        self.__path(svg_path, labels, style, z_index)

    def rectangle(self, p1, p2, z_index=1, **style):
        r = Rectangle(p1, p2)
        self.polygon([r.northwest, r.northeast, r.southeast, r.southwest], z_index=1, **style)

    def text(self, point, text, z_index=1, **style):

        def compute_anchors(position):
            if position == "center":
                x = 0
                y = 0
                valign = "central"
                align = "middle"
                return (x, y, align, valign)
            x = 0
            y = 0
            if position in ["above", "below"]:
                align = "middle"
                x = 0
            elif "left" in position:
                align = "end"
                x = -5
            else:
                x = 5
                align = "start"

            if position in ["left", "right"]:
                valign = "middle"
                y = 0
            elif "below" in position:
                valign = "hanging"
                y = 5
            else:
                valign = "text-top"
                y = -5
            return (x, y, align, valign)

        if "position" in style:
            position = style["position"]
            del style["position"]
        else:
            position = "center"
        (x, y, align, valign) = compute_anchors(position)

        text_style = {}
        self.parse_text_style(style, text_style)

        text_node = ET.Element("text", x=str(x), y=str(y), **text_style)
        text_node.set("text-anchor", align)
        text_node.set("dominant-baseline", valign)
        text_node.set("transform", f"translate({self.svgtransform(self.transform(point))})")
        text_node.text = str(text)
        self.add_to_layer(z_index, text_node)

    def edge(self, points, labels=None, closed=False, z_index=0, **style):

        tf = self.svgtransform * self.transform
        list_angles = self.find_angles(points, closed)
        if closed:
            points.append(points[0])
            list_angles.append(list_angles[0])

        angles = list(map(lambda x: x * math.pi / 180, list_angles))

        if "looseness" in style:
            looseness = style["looseness"]
            del style["looseness"]
        else:
            looseness = 1

        point = points[0]
        svg_path = SvgPath(tf(point))
        for i in range(len(points) - 1):
            newpoint = points[i + 1]
            dst = looseness * 0.3902 * newpoint.distance(point)
            fstcontrol = point + Point(dst, angles[i], polar=True)
            sndcontrol = newpoint - Point(dst, angles[i + 1], polar=True)
            svg_path.curve_to(tf(newpoint), tf(fstcontrol), tf(sndcontrol))
            point = newpoint

        self.__path(svg_path, labels, style, z_index)

    def polyline(self, points, labels=None, closed=False, z_index=0, **style):
        tf = self.svgtransform * self.transform

        def corners(p0, p1, p2):
            """returns points nears p1 to round the corners"""
            if p1.distance(p2) > p0.distance(p1):
                ratio = min(12, p1.distance(p2) / p0.distance(p1))
                t1 = 0.04 * ratio
                t2 = 0.04
            else:
                ratio = min(12, p0.distance(p1) / p1.distance(p2))
                t1 = 0.04
                t2 = 0.04 * ratio
            beforep1 = p0 * t1 + p1 * (1 - t1)
            afterp1 = p1 * (1 - t2) + p2 * t2
            return (beforep1, afterp1)

        if closed:
            points += [points[0]]

        if "rounded" in style and style["rounded"] and len(points) != 2:
            p2 = p1 = points[0]
            if closed:
                p0 = points[-2]
                p2 = points[1]
                (_, afterp1) = corners(p0, p1, p2)
                svg_path = SvgPath(tf(afterp1))
            else:
                svg_path = SvgPath(tf(p1))
            for i in range(len(points) - 2):
                p0 = points[i]
                p1 = points[i + 1]
                p2 = points[i + 2]
                (beforep1, afterp1) = corners(p0, p1, p2)
                svg_path.line_to(tf(beforep1))
                svg_path.quadratic_to(tf(afterp1), tf(p1))
            if not closed:
                svg_path.line_to(tf(p2))
            else:
                p0 = points[-2]
                p1 = points[0]
                p2 = points[1]
                (beforep1, afterp1) = corners(p0, p1, p2)
                svg_path.line_to(tf(beforep1))
                svg_path.quadratic_to(tf(afterp1), tf(p1))
        else:
            # not rounded
            svg_path = SvgPath(tf(points[0]))
            for point in points[1:]:
                svg_path.line_to(tf(point))

        self.__path(svg_path, labels, style, z_index)

    def draw(self, rect, fs=None, options=None, preamble=False):
        tf = self.svgtransform * self.transform
        rect = Rectangle.bounding_box(
            [*map(tf, [rect.northwest, rect.northeast, rect.southeast, rect.southwest])]
        )

        svg = ET.Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(rect.width),
            height=str(rect.height),
            viewBox=f"{rect.fst.x} {rect.fst.y} {rect.width} {rect.height}",
        )
        svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

        for i in sorted(self.layers.keys()):
            svg.extend(self.layers[i])

        print("\n".join(ET.tostringlist(svg, encoding="unicode")), file=fs)
